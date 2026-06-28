"""Two-mode LLM model resolver for ai-answers-searxng.

Modes:
- fixed (default): use LLM_MODEL exactly as configured.
- auto: discover the active chat model from an existing FastAPI/vLLM proxy.

No third-party dependencies. Detection failures always fall back safely.
"""
from __future__ import annotations

import http.client
import json
import logging
import os
import ssl
import threading
import time
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

_LOCK = threading.Lock()
_CACHE_MODEL = ""
_CACHE_EXPIRES_AT = 0.0
_CACHE_LAST_GOOD = ""


def _int(name: str, default: int, minimum: int = 1) -> int:
    try:
        return max(minimum, int(os.getenv(name, str(default))))
    except (TypeError, ValueError):
        return default


def _bool(name: str, default: bool = True) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _headers(api_key: str) -> dict[str, str]:
    headers = {"Accept": "application/json"}
    key = os.getenv("LLM_MODEL_API_KEY", "").strip() or api_key.strip()
    if key and key.lower() not in {"none", "ollama"}:
        name = os.getenv("LLM_MODEL_API_KEY_HEADER", "Authorization").strip() or "Authorization"
        scheme = os.getenv("LLM_MODEL_API_KEY_SCHEME", "Bearer").strip()
        headers[name] = f"{scheme} {key}".strip()
    return headers


def _get_json(url: str, headers: dict[str, str], timeout: float) -> Any:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"Invalid model discovery URL: {url!r}")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    if parsed.scheme == "https":
        context = ssl.create_default_context() if _bool("LLM_MODEL_VERIFY_SSL", True) else ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(parsed.hostname, port, timeout=timeout, context=context)
    else:
        conn = http.client.HTTPConnection(parsed.hostname, port, timeout=timeout)
    try:
        conn.request("GET", path, headers=headers)
        response = conn.getresponse()
        body = response.read()
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"HTTP {response.status}: {body.decode(errors='replace')[:500]}")
        return json.loads(body.decode("utf-8"))
    finally:
        conn.close()


def _chat_model_ids(models_response: Any) -> set[str]:
    if not isinstance(models_response, dict):
        return set()
    rows = models_response.get("data")
    if not isinstance(rows, list):
        return set()
    ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        model_id = str(row.get("id") or "").strip()
        task = str(row.get("task") or "").strip().lower()
        if model_id and task in {"chat.completions", "chat", "text-generation", "generation"}:
            ids.add(model_id)
    return ids


def _discover(default_model: str, api_key: str) -> str:
    status_url = os.getenv("LLM_SWITCH_STATUS_URL", "").strip()
    models_url = os.getenv("LLM_MODELS_URL", "").strip()
    timeout = float(_int("LLM_MODEL_DISCOVERY_TIMEOUT", 5))
    headers = _headers(api_key)

    candidate = ""
    if status_url:
        status = _get_json(status_url, headers, timeout)
        if isinstance(status, dict):
            candidate = str(status.get("active_model") or status.get("current_model") or "").strip()
            switching = bool(status.get("switching"))
            stage = str(status.get("stage") or "").strip()
            if candidate:
                logger.info(
                    "AI Answers model resolver: active=%s switching=%s stage=%s",
                    candidate,
                    switching,
                    stage,
                )

    # Validate against /v1/models when configured. Your proxy exposes task=chat.completions.
    if models_url:
        models = _get_json(models_url, headers, timeout)
        chat_ids = _chat_model_ids(models)
        if candidate and chat_ids and candidate not in chat_ids:
            raise RuntimeError(f"Active model {candidate!r} is not listed as a chat model")
        if not candidate and len(chat_ids) == 1:
            candidate = next(iter(chat_ids))

    if not candidate:
        raise RuntimeError("No active chat model was discovered")
    return candidate


def resolve_llm_model(default_model: str, api_key: str = "") -> str:
    """Return the model name to write into the outgoing chat payload."""
    mode = os.getenv("LLM_MODEL_MODE", "fixed").strip().lower()
    if mode not in {"auto", "dynamic"}:
        return default_model

    fallback = os.getenv("LLM_MODEL_FALLBACK", "").strip() or default_model
    ttl = _int("LLM_MODEL_CACHE_SECONDS", 15)
    now = time.monotonic()

    global _CACHE_MODEL, _CACHE_EXPIRES_AT, _CACHE_LAST_GOOD
    with _LOCK:
        if _CACHE_MODEL and now < _CACHE_EXPIRES_AT:
            return _CACHE_MODEL
        try:
            model = _discover(default_model, api_key)
            _CACHE_MODEL = model
            _CACHE_LAST_GOOD = model
            _CACHE_EXPIRES_AT = now + ttl
            return model
        except Exception as exc:
            # Stale last-good cache is preferable during a model switch or temporary proxy outage.
            if _CACHE_LAST_GOOD:
                logger.warning(
                    "AI Answers model resolver failed; using last active model %s: %s",
                    _CACHE_LAST_GOOD,
                    exc,
                )
                _CACHE_MODEL = _CACHE_LAST_GOOD
                _CACHE_EXPIRES_AT = now + min(ttl, 5)
                return _CACHE_LAST_GOOD
            logger.warning(
                "AI Answers model resolver failed; using fallback model %s: %s",
                fallback,
                exc,
            )
            return fallback
