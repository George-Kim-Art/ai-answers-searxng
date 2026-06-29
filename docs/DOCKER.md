# Docker Deployment Guide

This document explains how to run AI Answers with SearXNG using Docker Compose.

The examples are intentionally generic. They do not contain real API keys, private IP addresses, hostnames, model names or personal configuration.

## 1. Choose a Template

The `examples/` directory contains several templates:

```text
examples/
├── docker/      # Generic OpenAI-compatible deployment
├── openai/      # OpenAI hosted API
├── ollama/      # Local Ollama OpenAI-compatible endpoint
├── oneapi/      # OneAPI / NewAPI gateway
├── litellm/     # LiteLLM gateway
└── vllm/        # vLLM OpenAI-compatible server
```

If you are not sure which one to use, start with:

```bash
cd examples/docker
```

## 2. Create `.env`

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```env
LLM_URL=https://api.openai.com/v1/chat/completions
LLM_KEY=your_api_key
LLM_MODEL=gpt-4o-mini
```

For local gateways, replace `LLM_URL` with the gateway chat completions endpoint.

Examples:

```env
# OpenAI
LLM_URL=https://api.openai.com/v1/chat/completions

# Ollama OpenAI-compatible endpoint
LLM_URL=http://host.docker.internal:11434/v1/chat/completions

# vLLM
LLM_URL=http://host.docker.internal:8000/v1/chat/completions

# OneAPI / NewAPI / LiteLLM
LLM_URL=http://host.docker.internal:3000/v1/chat/completions
```

## 3. Start SearXNG

```bash
docker compose up -d
```

Check logs:

```bash
docker compose logs -f searxng
```

Open:

```text
http://localhost:8080
```

## 4. Plugin Files Mounted by Docker

The examples mount the plugin files into the SearXNG container:

```yaml
volumes:
  - ../../plugins/ai_answers.py:/etc/searxng/plugins/ai_answers.py:ro
  - ../../plugins/semantic_rank.py:/etc/searxng/plugins/semantic_rank.py:ro
  - ../../plugins/model_resolver.py:/etc/searxng/plugins/model_resolver.py:ro
```

If your SearXNG image uses a different plugin path, adjust the mount path.

## 5. Environment Variables

All examples load variables through:

```yaml
env_file:
  - .env
```

Keep real `.env` files out of Git. Only commit `.env.example`.

## 6. Enabling Semantic Retrieval

Semantic retrieval is disabled by default.

Enable it:

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=http://host.docker.internal:8081/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
```

The endpoint should accept an OpenAI-compatible embeddings payload:

```json
{
  "model": "text-embedding-3-small",
  "input": ["text 1", "text 2"]
}
```

## 7. Enabling Rerank

Rerank is disabled by default.

TEI-style example:

```env
RERANK_ENABLED=true
RERANK_API_FORMAT=tei
RERANK_URL=http://host.docker.internal:8082/rerank
RERANK_MODEL=BAAI/bge-reranker-v2-m3
```

Jina example:

```env
RERANK_ENABLED=true
RERANK_API_FORMAT=jina
RERANK_URL=https://api.jina.ai/v1/rerank
RERANK_MODEL=jina-reranker-v2-base-multilingual
RERANK_API_KEY=your_jina_key
```

Cohere-compatible example:

```env
RERANK_ENABLED=true
RERANK_API_FORMAT=cohere
RERANK_URL=https://api.cohere.com/v1/rerank
RERANK_MODEL=rerank-multilingual-v3.0
RERANK_API_KEY=your_cohere_key
```

## 8. Docker Networking Notes

From inside a Docker container, `localhost` means the container itself.

Use one of these instead:

- `host.docker.internal` for Docker Desktop and many modern Docker setups
- the Docker Compose service name if the model service is in the same compose file
- the host machine LAN IP for Linux setups where `host.docker.internal` is not available

For Linux, the examples include:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

## 9. Troubleshooting

### The plugin cannot reach the model server

Check the endpoint from inside the container:

```bash
docker compose exec searxng sh
wget -qO- http://host.docker.internal:8000/v1/models
```

### Embedding is enabled but results look unchanged

Check:

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=...
EMBEDDING_MODEL=...
```

Also check logs for:

```text
AI Answers retrieval
```

### Rerank fails silently

The plugin is designed to fail open. If rerank fails, it falls back to the existing ranking instead of breaking search.

Check:

```env
RERANK_API_FORMAT=tei|jina|cohere
RERANK_URL=...
RERANK_MODEL=...
```

### Do not commit secrets

Before opening a PR, verify:

```bash
git status --ignored
```

Make sure `.env` is ignored and only `.env.example` is committed.
