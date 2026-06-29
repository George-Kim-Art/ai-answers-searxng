# Installation

This guide covers manual installation without Docker.

For Docker deployment, see [DOCKER.md](DOCKER.md).

## 1. Copy Plugin Files

Copy these files into your SearXNG plugin directory:

```text
plugins/
├── ai_answers.py
├── semantic_rank.py
└── model_resolver.py
```

Depending on your SearXNG installation, the plugin directory may be similar to:

```text
/etc/searxng/plugins/
```

or a local development path.

## 2. Enable the Plugin

Merge the example settings into your SearXNG `settings.yml`.

Minimal example:

```yaml
use_default_settings: true

enabled_plugins:
  - ai_answers
```

If your upstream SearXNG build uses a different plugin activation format, follow that format and only copy the plugin files from this project.

## 3. Configure the LLM

Set environment variables for the SearXNG process.

Minimal OpenAI-compatible example:

```env
LLM_PROVIDER=openai
LLM_URL=https://api.openai.com/v1/chat/completions
LLM_KEY=your_api_key
LLM_MODEL=gpt-4o-mini
LLM_MODEL_MODE=fixed

EMBEDDING_ENABLED=false
RERANK_ENABLED=false
```

## 4. Restart SearXNG

Restart your SearXNG service after copying files or changing environment variables.

Example systemd command:

```bash
sudo systemctl restart searxng
```

Docker users should use:

```bash
docker compose restart searxng
```

## 5. Verify

Open SearXNG and run a normal search query.

If AI Answers does not appear:

1. Check that the plugin file is in the correct directory.
2. Check `settings.yml` plugin activation.
3. Check SearXNG logs.
4. Check that the LLM endpoint is reachable from the SearXNG process.

## 6. Optional: Enable Embedding Retrieval

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=https://api.openai.com/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your_api_key
```

## 7. Optional: Enable Rerank

```env
RERANK_ENABLED=true
RERANK_API_FORMAT=tei
RERANK_URL=http://localhost:8082/rerank
RERANK_MODEL=BAAI/bge-reranker-v2-m3
```

## 8. Optional: Enable Auto Model Discovery

```env
LLM_MODEL_MODE=auto
LLM_MODELS_URL=http://localhost:8000/v1/models
LLM_MODEL_FALLBACK=gpt-4o-mini
```

## Installation Checklist

Before reporting issues, confirm:

- `ai_answers.py` exists in the plugin directory.
- `semantic_rank.py` exists next to `ai_answers.py`.
- `model_resolver.py` exists next to `ai_answers.py`.
- SearXNG can read those files.
- Environment variables are available to the SearXNG process.
- The LLM endpoint is reachable from the SearXNG host/container.
