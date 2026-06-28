"""Optional embedding + reranker pipeline for ai-answers-searxng.

No third-party Python dependencies. Supports OpenAI-compatible embeddings and
common rerank APIs (TEI/Jina/Cohere-style response shapes). Failures always
fall back to the incoming SearXNG order.
"""
from __future__ import annotations

import http.client
import json
import logging
import math
import os
import ssl
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

_TRUE = {"1", "true", "yes", "on"}


def _bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in _TRUE


def _int(name: str, default: int, minimum: int = 1) -> int:
    try:
        return max(minimum, int(os.getenv(name, str(default))))
    except (TypeError, ValueError):
        return default


def _float(name: str, default: float, minimum: float = 0.1) -> float:
    try:
        return max(minimum, float(os.getenv(name, str(default))))
    except (TypeError, ValueError):
        return default


def _headers(prefix: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    key = os.getenv(f"{prefix}_API_KEY", "").strip()
    header_name = os.getenv(f"{prefix}_API_KEY_HEADER", "Authorization").strip()
    scheme = os.getenv(f"{prefix}_API_KEY_SCHEME", "Bearer").strip()
    if key:
        headers[header_name] = f"{scheme} {key}".strip()
    return headers


def _post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: float) -> Any:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError(f"Invalid API URL: {url!r}")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    if parsed.scheme == "https":
        verify = _bool("RETRIEVAL_VERIFY_SSL", True)
        context = ssl.create_default_context() if verify else ssl._create_unverified_context()
        conn = http.client.HTTPSConnection(parsed.hostname, port, timeout=timeout, context=context)
    else:
        conn = http.client.HTTPConnection(parsed.hostname, port, timeout=timeout)
    try:
        conn.request("POST", path, body=json.dumps(payload, ensure_ascii=False).encode(), headers=headers)
        response = conn.getresponse()
        body = response.read()
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"HTTP {response.status}: {body.decode(errors='replace')[:500]}")
        return json.loads(body.decode("utf-8"))
    finally:
        conn.close()


def _text(item: dict[str, Any]) -> str:
    title = str(item.get("title") or "").strip()
    content = str(item.get("content") or "").strip()
    max_chars = _int("RETRIEVAL_DOCUMENT_MAX_CHARS", 3000, 200)
    return f"{title}\n{content}".strip()[:max_chars]


def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return -1.0
    dot = sum(float(x) * float(y) for x, y in zip(a, b))
    na = math.sqrt(sum(float(x) ** 2 for x in a))
    nb = math.sqrt(sum(float(y) ** 2 for y in b))
    return dot / (na * nb) if na and nb else -1.0


def _extract_embeddings(response: Any) -> list[list[float]]:
    # OpenAI-compatible: {"data":[{"index":0,"embedding":[...]}]}
    if isinstance(response, dict) and isinstance(response.get("data"), list):
        rows = response["data"]
        indexed = sorted(rows, key=lambda row: int(row.get("index", 0)))
        return [row["embedding"] for row in indexed if isinstance(row.get("embedding"), list)]
    # Some local servers: {"embeddings":[[...], ...]}
    if isinstance(response, dict) and isinstance(response.get("embeddings"), list):
        return response["embeddings"]
    # Ollama-style single or batch responses
    if isinstance(response, dict) and isinstance(response.get("embedding"), list):
        return [response["embedding"]]
    raise RuntimeError("Unsupported embedding response shape")


def embedding_filter(query: str, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not _bool("EMBEDDING_ENABLED", False) or len(results) < 2:
        return results
    url = os.getenv("EMBEDDING_URL", "").strip()
    if not url:
        logger.warning("AI Answers retrieval: EMBEDDING_ENABLED=true but EMBEDDING_URL is empty")
        return results
    texts = [query] + [_text(item) for item in results]
    provider = os.getenv("EMBEDDING_API_FORMAT", "openai").strip().lower()
    model = os.getenv("EMBEDDING_MODEL", "").strip()
    if provider == "ollama":
        payload = {"model": model, "input": texts}
    else:
        payload = {"input": texts}
        if model:
            payload["model"] = model
    try:
        response = _post_json(url, payload, _headers("EMBEDDING"), _float("RETRIEVAL_TIMEOUT", 10.0))
        vectors = _extract_embeddings(response)
        if len(vectors) != len(texts):
            raise RuntimeError(f"Expected {len(texts)} embeddings, got {len(vectors)}")
        query_vector = vectors[0]
        ranked = []
        for item, vector in zip(results, vectors[1:]):
            copy = dict(item)
            copy["_embedding_score"] = _cosine(query_vector, vector)
            ranked.append(copy)
        ranked.sort(key=lambda x: x.get("_embedding_score", -1.0), reverse=True)
        top_k = min(_int("EMBEDDING_TOP_K", 15), len(ranked))
        logger.info("AI Answers retrieval: embedding kept %d/%d", top_k, len(results))
        return ranked[:top_k]
    except Exception as exc:
        logger.warning("AI Answers retrieval: embedding failed, fallback to SearXNG order: %s", exc)
        return results


def _extract_ranking(response: Any) -> list[dict[str, Any]]:
    if isinstance(response, list):
        return response
    if isinstance(response, dict):
        for key in ("results", "data", "rankings"):
            if isinstance(response.get(key), list):
                return response[key]
    raise RuntimeError("Unsupported reranker response shape")


def rerank(query: str, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not _bool("RERANK_ENABLED", False) or len(results) < 2:
        return results
    url = os.getenv("RERANK_URL", "").strip()
    if not url:
        logger.warning("AI Answers retrieval: RERANK_ENABLED=true but RERANK_URL is empty")
        return results
    documents = [_text(item) for item in results]
    model = os.getenv("RERANK_MODEL", "").strip()
    api_format = os.getenv("RERANK_API_FORMAT", "tei").strip().lower()
    top_k = min(_int("RERANK_TOP_K", 8), len(results))
    if api_format == "cohere":
        payload = {"query": query, "documents": documents, "top_n": top_k}
    elif api_format == "jina":
        payload = {"query": query, "documents": documents, "top_n": top_k, "return_documents": False}
    else:  # Hugging Face TEI and many compatible servers
        payload = {"query": query, "texts": documents, "truncate": True, "return_text": False}
    if model:
        payload["model"] = model
    try:
        response = _post_json(url, payload, _headers("RERANK"), _float("RETRIEVAL_TIMEOUT", 10.0))
        rows = _extract_ranking(response)
        ranked: list[dict[str, Any]] = []
        used: set[int] = set()
        for row in rows:
            index = row.get("index", row.get("document_index"))
            if index is None and isinstance(row.get("document"), dict):
                index = row["document"].get("index")
            if index is None:
                continue
            index = int(index)
            if index < 0 or index >= len(results) or index in used:
                continue
            copy = dict(results[index])
            copy["_reranker_score"] = float(row.get("relevance_score", row.get("score", 0.0)))
            ranked.append(copy)
            used.add(index)
        if not ranked:
            raise RuntimeError("Reranker returned no usable indexed results")
        # APIs normally return sorted rows, but sort defensively.
        ranked.sort(key=lambda x: x.get("_reranker_score", 0.0), reverse=True)
        logger.info("AI Answers retrieval: reranker kept %d/%d", min(top_k, len(ranked)), len(results))
        return ranked[:top_k]
    except Exception as exc:
        logger.warning("AI Answers retrieval: reranker failed, fallback to previous order: %s", exc)
        return results


def semantic_rank(query: str, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Run optional embedding recall then optional reranking."""
    if not query or not results:
        return results
    candidate_count = _int("RETRIEVAL_CANDIDATE_COUNT", 25)
    candidates = results[:candidate_count]
    candidates = embedding_filter(query, candidates)
    candidates = rerank(query, candidates)
    return candidates
