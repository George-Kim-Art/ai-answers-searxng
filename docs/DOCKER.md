# Docker Deployment

This document provides a reference Docker Compose deployment for SearXNG with the
AI Answers plugin and its optional retrieval modules.

The example is intentionally generic. It does not contain real API keys, private
IP addresses, internal domains, or personal deployment details.

## File layout

A typical checkout should look like this:

```text
.
├── plugins/
│   ├── ai_answers.py
│   ├── semantic_rank.py
│   └── model_resolver.py
├── searxng/
│   └── settings.yml
├── examples/
│   └── docker/
│       ├── docker-compose.yml
│       └── .env.example
└── .env
```

## Quick start

Copy the example environment file:

```bash
cp examples/docker/.env.example .env
```

Edit `.env` and configure at least:

```env
LLM_KEY=replace-with-your-api-key
LLM_URL=https://api.example.com/v1/chat/completions
LLM_MODEL=example-chat-model
```

Start SearXNG:

```bash
docker compose -f examples/docker/docker-compose.yml --env-file .env up -d
```

Open:

```text
http://localhost:18080/
```

## Minimal mode

Minimal mode keeps the original behavior and disables semantic retrieval:

```env
LLM_MODEL_MODE=fixed
EMBEDDING_ENABLED=false
RERANK_ENABLED=false
```

This is the recommended first test.

## Embedding mode

Enable semantic retrieval after the base plugin works:

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=https://api.example.com/v1/embeddings
EMBEDDING_MODEL=example-embedding-model
EMBEDDING_API_FORMAT=openai
EMBEDDING_API_KEY=replace-with-your-api-key
```

Any provider exposing an OpenAI-compatible embeddings endpoint can be used.

## Rerank mode

Enable reranking after embedding retrieval works:

```env
RERANK_ENABLED=true
RERANK_URL=https://api.example.com/v1/rerank
RERANK_MODEL=example-rerank-model
RERANK_API_FORMAT=cohere
RERANK_API_KEY=replace-with-your-api-key
```

Supported rerank API formats include:

- `tei`
- `jina`
- `cohere`

Services exposing Cohere-compatible rerank endpoints can usually use
`RERANK_API_FORMAT=cohere`.

## Dynamic model resolver

Fixed mode is the default:

```env
LLM_MODEL_MODE=fixed
LLM_MODEL=example-chat-model
```

Auto mode can be used with model-switching gateways or OpenAI-compatible model
list endpoints:

```env
LLM_MODEL_MODE=auto
LLM_MODEL_FALLBACK=example-chat-model
LLM_MODELS_URL=https://api.example.com/v1/models
```

If discovery fails, the plugin falls back to `LLM_MODEL_FALLBACK` or `LLM_MODEL`.

## Mounted files

The Docker Compose example mounts the plugin modules directly into the SearXNG
container:

```yaml
- ../../plugins/ai_answers.py:/usr/local/searxng/searx/plugins/ai_answers.py:ro
- ../../plugins/semantic_rank.py:/usr/local/searxng/searx/plugins/semantic_rank.py:ro
- ../../plugins/model_resolver.py:/usr/local/searxng/searx/plugins/model_resolver.py:ro
```

All three files are required because `ai_answers.py` imports the helper modules.

## Security notes

Do not commit:

- `.env`
- real API keys
- private IP addresses
- internal domains
- personal paths
- backup files
- logs

Only commit `.env.example` with safe placeholder values.
