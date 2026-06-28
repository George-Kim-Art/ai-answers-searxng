# Installation

## Basic installation

Copy the plugin files into the SearXNG plugin directory:

```text
searxng/plugins/
├── ai_answers.py
├── semantic_rank.py
└── model_resolver.py
```

Then enable the plugin in the SearXNG settings as usual.

## Minimal configuration

No new configuration is required for the original behavior.

```env
LLM_PROVIDER=openai
LLM_KEY=your-api-key
LLM_MODEL=gpt-4o-mini
```

If semantic retrieval and reranking are not enabled, the plugin uses the normal SearXNG result order.

## Enable semantic retrieval

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=https://example.com/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your-embedding-key
```

## Enable reranking

```env
RERANK_ENABLED=true
RERANK_URL=https://example.com/rerank
RERANK_MODEL=your-rerank-model
RERANK_API_FORMAT=tei
```

## Enable dynamic model discovery

```env
LLM_MODEL_MODE=auto
LLM_MODELS_URL=https://example.com/v1/models
LLM_MODEL_FALLBACK=gpt-4o-mini
```

When auto mode fails, the plugin falls back to the configured model.
