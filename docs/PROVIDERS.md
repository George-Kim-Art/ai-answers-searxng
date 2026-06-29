# Supported Providers

The plugin is provider-neutral whenever possible. It relies on HTTP APIs and does not require provider-specific Python SDKs.

## LLM Providers

The main LLM call expects an OpenAI-style chat completions endpoint.

| Provider / Gateway | Supported | Notes |
|---|---:|---|
| OpenAI | Yes | Use `/v1/chat/completions`. |
| Ollama | Yes | Use Ollama's OpenAI-compatible endpoint. |
| vLLM | Yes | Use vLLM OpenAI-compatible server. |
| LiteLLM | Yes | Use LiteLLM proxy `/v1/chat/completions`. |
| OneAPI | Yes | OpenAI-compatible gateway. |
| NewAPI | Yes | OpenAI-compatible gateway. |
| SiliconFlow | Yes | OpenAI-compatible API style. |
| Local gateways | Yes | Any endpoint compatible with OpenAI chat completions. |

## Embedding Providers

Embedding support is built around OpenAI-compatible embeddings requests.

Expected request shape:

```json
{
  "model": "embedding-model-name",
  "input": ["query text", "document text"]
}
```

Expected response shape:

```json
{
  "data": [
    {"embedding": [0.1, 0.2, 0.3]},
    {"embedding": [0.2, 0.1, 0.4]}
  ]
}
```

| Provider / Gateway | Supported | Notes |
|---|---:|---|
| OpenAI embeddings | Yes | `text-embedding-3-small`, `text-embedding-3-large`, etc. |
| Ollama via compatible endpoint | Yes | Requires an OpenAI-compatible embeddings path. |
| TEI embeddings | Usually | Works if exposed with OpenAI-compatible response format. |
| vLLM embeddings | Usually | Depends on model and server configuration. |
| LiteLLM | Yes | Proxies many embedding providers. |
| OneAPI / NewAPI | Yes | If embeddings endpoint is enabled. |
| Local embedding gateway | Yes | Must return OpenAI-compatible embedding arrays. |

## Rerank Providers

Rerank supports multiple API payload styles through `RERANK_API_FORMAT`.

| Format | Variable | Typical Endpoint | Notes |
|---|---|---|---|
| TEI | `RERANK_API_FORMAT=tei` | `/rerank` | Good for local Hugging Face TEI rerank servers. |
| Jina | `RERANK_API_FORMAT=jina` | `/v1/rerank` | Works with Jina AI reranker API. |
| Cohere-compatible | `RERANK_API_FORMAT=cohere` | `/v1/rerank` | Works with Cohere and compatible services. |

## Provider Selection Guide

### I use OpenAI only

Use:

```env
LLM_URL=https://api.openai.com/v1/chat/completions
LLM_KEY=your_openai_key
LLM_MODEL=gpt-4o-mini

EMBEDDING_ENABLED=true
EMBEDDING_URL=https://api.openai.com/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your_openai_key
```

### I use a local LLM gateway

Use the gateway's OpenAI-compatible endpoint:

```env
LLM_URL=http://host.docker.internal:8000/v1/chat/completions
LLM_KEY=
LLM_MODEL=local-model
```

### I want best retrieval quality

Use both embeddings and rerank:

```env
EMBEDDING_ENABLED=true
RERANK_ENABLED=true
```

A common setup is:

- LLM: OpenAI-compatible chat model
- Embedding: BGE-M3 or OpenAI embedding model
- Rerank: BGE reranker, Jina reranker, or Cohere-compatible reranker

## Adding a New Provider

If the provider already supports OpenAI-compatible APIs, no code changes should be needed.

If it uses a custom API format:

1. Add a new `*_API_FORMAT` option.
2. Convert the provider request into the common internal shape.
3. Convert the provider response back into a list of scores or embeddings.
4. Document the provider here.
5. Add a template under `examples/` if useful.
