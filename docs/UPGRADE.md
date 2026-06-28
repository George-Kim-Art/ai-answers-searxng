# Upgrade Guide

## From the original single-file plugin

1. Replace the old plugin file with the updated `ai_answers.py`.
2. Add the helper modules:

```text
plugins/
├── ai_answers.py
├── semantic_rank.py
└── model_resolver.py
```

3. Restart SearXNG.

No new environment variables are required for the old behavior.

## Enabling new features after upgrade

Enable semantic retrieval only when an embedding endpoint is available:

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=https://example.com/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
```

Enable reranking only when a rerank endpoint is available:

```env
RERANK_ENABLED=true
RERANK_URL=https://example.com/rerank
RERANK_API_FORMAT=tei
```

## Rollback

To roll back, restore the previous `ai_answers.py` and remove:

```text
semantic_rank.py
model_resolver.py
```
