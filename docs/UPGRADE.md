# Upgrade Guide

This document explains how to update this plugin while keeping local configuration safe.

## Important Rule

Do not edit committed example files with real secrets.

Use:

```text
.env                 # local, ignored by Git
.env.example         # committed template, no secrets
```

## Updating Plugin Files

Replace these files with the new version:

```text
plugins/ai_answers.py
plugins/semantic_rank.py
plugins/model_resolver.py
```

Then restart SearXNG.

## Updating Docker Examples

If you are using an example deployment directory:

```bash
cd examples/docker
cp .env.example .env
```

Only do this the first time. If you already have a local `.env`, compare it manually with the new `.env.example` and copy new variables as needed.

## Migrating from Fixed Model to Auto Model

Old fixed mode:

```env
LLM_MODEL_MODE=fixed
LLM_MODEL=gpt-4o-mini
```

New auto mode:

```env
LLM_MODEL_MODE=auto
LLM_MODEL_FALLBACK=gpt-4o-mini
LLM_MODELS_URL=http://host.docker.internal:8000/v1/models
```

If auto discovery fails, the plugin falls back to `LLM_MODEL_FALLBACK`.

## Migrating to Semantic Retrieval

Start with embeddings only:

```env
EMBEDDING_ENABLED=true
EMBEDDING_TOP_K=15
RERANK_ENABLED=false
```

After confirming embeddings work, enable rerank:

```env
RERANK_ENABLED=true
RERANK_TOP_K=8
```

This staged approach makes troubleshooting easier.

## Compatibility Notes

Default values preserve old behavior:

```env
LLM_MODEL_MODE=fixed
EMBEDDING_ENABLED=false
RERANK_ENABLED=false
```

So existing users can upgrade files first, then enable new features later.

## Rollback

If a new version causes issues:

1. Restore previous plugin files.
2. Restart SearXNG.
3. Disable optional retrieval variables if needed:

```env
EMBEDDING_ENABLED=false
RERANK_ENABLED=false
LLM_MODEL_MODE=fixed
```
