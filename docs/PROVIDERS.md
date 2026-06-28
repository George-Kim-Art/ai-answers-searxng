# Retrieval Providers

## Embedding providers

The embedding client expects an OpenAI-compatible response shape:

```json
{
  "data": [
    {"embedding": [0.1, 0.2, 0.3]}
  ]
}
```

This makes the integration provider-neutral. It can work with hosted providers, local gateways, and self-hosted model servers as long as the endpoint implements the expected API shape.

Known compatible API styles:

| API style | Notes |
| --- | --- |
| OpenAI embeddings | Native target format |
| vLLM OpenAI-compatible API | Works when embeddings are enabled by the server |
| LiteLLM | Works through its OpenAI-compatible proxy |
| OneAPI / NewAPI | Works through OpenAI-compatible routing |
| Local gateways | Works if they expose `/v1/embeddings` |

## Rerank providers

The reranker supports multiple request and response styles.

| `RERANK_API_FORMAT` | Description |
| --- | --- |
| `tei` | Text Embeddings Inference rerank API style |
| `jina` | Jina AI rerank API style |
| `cohere` | Cohere-compatible rerank API style |

## Recommended pipeline

```text
SearXNG results
    │
    ▼
Candidate extraction
    │
    ▼
Embedding similarity ranking
    │
    ▼
Optional reranker
    │
    ▼
Prompt context
```

Embedding ranking improves recall. Reranking improves precision.
