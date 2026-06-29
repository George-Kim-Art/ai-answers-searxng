# Development and Maintenance Guide

This document is for future maintainers who want to modify or extend the AI Answers plugin.

## Design Principles

The extension follows five principles:

1. Keep `ai_answers.py` as the orchestration layer.
2. Keep provider-specific retrieval logic in `semantic_rank.py`.
3. Keep model selection logic in `model_resolver.py`.
4. Make new features optional and fail-open.
5. Avoid leaking deployment-specific configuration into the repository.

## File Responsibilities

### `plugins/ai_answers.py`

Main SearXNG plugin file.

Responsibilities:

- Reads plugin configuration from environment variables.
- Receives search results from SearXNG.
- Builds LLM prompts.
- Calls the configured LLM endpoint.
- Calls optional helpers when configured.

This file should avoid provider-specific embedding or rerank logic when possible.

### `plugins/semantic_rank.py`

Retrieval helper.

Responsibilities:

- Convert search results into rankable text documents.
- Call an embeddings endpoint when `EMBEDDING_ENABLED=true`.
- Compute cosine similarity between query and result embeddings.
- Keep only the top embedding candidates.
- Call an optional reranker when `RERANK_ENABLED=true`.
- Return a reordered result list.

Important behavior:

- If embedding fails, the original result order is preserved.
- If rerank fails, the embedding-ranked or original result order is preserved.
- No additional Python package is required.

### `plugins/model_resolver.py`

Model selection helper.

Responsibilities:

- Fixed model mode.
- Automatic model discovery mode.
- `/v1/models` discovery.
- Optional status endpoint discovery.
- Cache discovered model names.
- Fallback to a configured model.

Important behavior:

- Default mode is fixed.
- Auto mode must never block normal plugin operation for long.
- Discovery failure falls back to `LLM_MODEL_FALLBACK` or `LLM_MODEL`.

## Runtime Flow

```text
Search request
    │
    ▼
ai_answers.py
    │
    ├─ read environment configuration
    ├─ resolve current model through model_resolver.py
    ├─ receive SearXNG search results
    ├─ optionally rank candidates through semantic_rank.py
    ├─ build prompt from selected results
    └─ call LLM endpoint
```

## Adding a New Embedding Provider

Prefer OpenAI-compatible endpoints whenever possible.

If a provider needs a different payload shape:

1. Add a new `EMBEDDING_API_FORMAT` value.
2. Keep the default `openai` behavior unchanged.
3. Add a small payload adapter in `semantic_rank.py`.
4. Document the provider in `docs/PROVIDERS.md`.
5. Add an example `.env.example` if the provider is common.

Do not hardcode API keys, local IPs or model names.

## Adding a New Rerank Provider

Current supported formats:

- `tei`
- `jina`
- `cohere`

To add another provider:

1. Add a new `RERANK_API_FORMAT` value.
2. Implement only the request/response adapter.
3. Normalize returned scores into a common sorted result list.
4. Preserve fail-open behavior.
5. Update `docs/PROVIDERS.md` and `docs/CONFIGURATION.md`.

## Error Handling Rules

Retrieval and discovery are optional features. They should not break normal search.

Use this behavior:

- Configuration missing: log warning and skip optional feature.
- Endpoint timeout: log warning and fall back.
- Response parse failure: log warning and fall back.
- LLM call failure: return the existing plugin error behavior.

## Security Rules

Never commit:

- `.env`
- real API keys
- private URLs
- internal hostnames
- local IP addresses
- personal model names if they identify a private deployment
- logs
- cache files
- backup files

Commit only `.env.example` files with placeholders.

## Testing Before PR

Run Python syntax checks:

```bash
python -m py_compile plugins/ai_answers.py plugins/semantic_rank.py plugins/model_resolver.py
```

Check the package contents:

```bash
find . -type f | sort
```

Check for secrets manually:

```bash
grep -R "sk-\|api_key\|password\|192\.168\.\|10\.\|172\.16\." . \
  --exclude-dir=.git \
  --exclude='*.md'
```

The grep command is only a rough check. Review files manually before publishing.

## Recommended PR Split

For easier review:

1. Documentation and Docker examples.
2. Model resolver.
3. Semantic retrieval and rerank.

This makes the review smaller and gives upstream maintainers a chance to discuss architecture before reviewing the full retrieval pipeline.
