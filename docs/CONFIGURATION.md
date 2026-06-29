# Configuration Reference

The plugin is configured with environment variables.

Most options are optional. The safest minimal setup is a fixed LLM model with retrieval disabled.

## Minimal Configuration

```env
LLM_PROVIDER=openai
LLM_URL=https://api.openai.com/v1/chat/completions
LLM_KEY=your_api_key
LLM_MODEL=gpt-4o-mini

EMBEDDING_ENABLED=false
RERANK_ENABLED=false
LLM_MODEL_MODE=fixed
```

## LLM Options

| Variable | Default | Description |
|---|---:|---|
| `LLM_PROVIDER` | empty | Provider preset name. Use `openai`, `ollama`, or leave empty and configure `LLM_URL` directly. |
| `LLM_URL` | provider default | Chat completions endpoint. Usually ends with `/v1/chat/completions`. |
| `LLM_KEY` | empty | API key for the LLM endpoint. Leave empty only for trusted local services. |
| `LLM_MODEL` | provider default | Model name used in fixed mode and as fallback in auto mode. |
| `LLM_MAX_TOKENS` | `500` | Maximum output tokens requested from the LLM. |
| `LLM_TEMPERATURE` | `0.2` | LLM sampling temperature. Lower values are more deterministic. |
| `LLM_SYSTEM_PROMPT` | empty | Optional extra system instruction. |
| `LLM_INTERACTIVE` | `true` | Enables interactive behavior if supported by the plugin. |
| `LLM_QUESTION_MARK_REQUIRED` | `false` | Require a question mark before triggering the plugin. |
| `LLM_TABS` | plugin default | Comma-separated SearXNG tabs where AI Answers is allowed. |
| `LLM_CONTEXT_DEEP_COUNT` | `5` | Number of deeper context items used by the prompt builder. |
| `LLM_CONTEXT_SHALLOW_COUNT` | `15` | Number of shallow context items considered. |
| `LLM_OLLAMA_UNLOAD_AFTER` | `false` | Ollama-specific behavior if supported by the deployment. |

## Model Resolver Options

Model resolver supports two modes:

- `fixed`: always use `LLM_MODEL`
- `auto`: try to discover the active model, then fall back to `LLM_MODEL_FALLBACK` or `LLM_MODEL`

| Variable | Default | Description |
|---|---:|---|
| `LLM_MODEL_MODE` | `fixed` | `fixed` or `auto`. |
| `LLM_MODEL_FALLBACK` | `LLM_MODEL` | Fallback model if auto discovery fails. |
| `LLM_MODELS_URL` | empty | OpenAI-compatible `/v1/models` endpoint used for discovery. |
| `LLM_SWITCH_STATUS_URL` | empty | Optional status endpoint for gateways that expose current model state. |
| `LLM_MODEL_CACHE_SECONDS` | `15` | Cache TTL for discovered model names. |
| `LLM_MODEL_DISCOVERY_TIMEOUT` | `5` | Timeout for model discovery requests. |
| `LLM_MODEL_API_KEY` | `LLM_KEY` | Optional separate API key for discovery endpoints. |
| `LLM_MODEL_API_KEY_HEADER` | `Authorization` | Header used for model discovery auth. |
| `LLM_MODEL_API_KEY_SCHEME` | `Bearer` | Auth scheme prefix. Set empty if the endpoint expects a raw key. |
| `LLM_MODEL_VERIFY_SSL` | `true` | Verify TLS certificates for model discovery. Disable only for trusted internal deployments. |

### Fixed Mode Example

```env
LLM_MODEL_MODE=fixed
LLM_MODEL=gpt-4o-mini
```

### Auto Mode Example

```env
LLM_MODEL_MODE=auto
LLM_MODEL_FALLBACK=gpt-4o-mini
LLM_MODELS_URL=http://host.docker.internal:8000/v1/models
LLM_MODEL_CACHE_SECONDS=60
```

## Semantic Retrieval Options

Semantic retrieval ranks search results using embeddings.

It is disabled by default.

| Variable | Default | Description |
|---|---:|---|
| `EMBEDDING_ENABLED` | `false` | Enable embedding-based ranking. |
| `EMBEDDING_URL` | empty | Embeddings endpoint. Usually ends with `/v1/embeddings`. |
| `EMBEDDING_MODEL` | empty | Embedding model name. |
| `EMBEDDING_API_FORMAT` | `openai` | Embedding API format. Currently OpenAI-compatible is the default. |
| `EMBEDDING_API_KEY` | empty | API key for embedding endpoint. |
| `EMBEDDING_API_KEY_HEADER` | `Authorization` | Header used for embedding auth. |
| `EMBEDDING_API_KEY_SCHEME` | `Bearer` | Auth scheme prefix. |
| `EMBEDDING_TOP_K` | `15` | Number of embedding-ranked candidates passed forward. |

Example:

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=https://api.openai.com/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your_api_key
EMBEDDING_TOP_K=15
```

## Rerank Options

Rerank reorders candidate documents after search or embedding ranking.

It is disabled by default.

| Variable | Default | Description |
|---|---:|---|
| `RERANK_ENABLED` | `false` | Enable reranking. |
| `RERANK_URL` | empty | Rerank endpoint. |
| `RERANK_MODEL` | empty | Rerank model name. |
| `RERANK_API_FORMAT` | `tei` | `tei`, `jina`, or `cohere`. |
| `RERANK_API_KEY` | empty | API key for rerank endpoint. |
| `RERANK_API_KEY_HEADER` | `Authorization` | Header used for rerank auth. |
| `RERANK_API_KEY_SCHEME` | `Bearer` | Auth scheme prefix. |
| `RERANK_TOP_K` | `8` | Number of reranked items kept for prompt construction. |

TEI example:

```env
RERANK_ENABLED=true
RERANK_API_FORMAT=tei
RERANK_URL=http://host.docker.internal:8082/rerank
RERANK_MODEL=BAAI/bge-reranker-v2-m3
RERANK_TOP_K=8
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

## Retrieval Runtime Options

| Variable | Default | Description |
|---|---:|---|
| `RETRIEVAL_CANDIDATE_COUNT` | `25` | Number of search results considered by the retrieval helper. |
| `RETRIEVAL_DOCUMENT_MAX_CHARS` | `3000` | Maximum characters extracted from each result for embedding/rerank. |
| `RETRIEVAL_TIMEOUT` | `10` | Timeout for embedding and rerank requests. |
| `RETRIEVAL_VERIFY_SSL` | `true` | Verify TLS certificates for retrieval endpoints. Disable only for trusted internal endpoints. |

## Recommended Presets

### Fast and Simple

```env
EMBEDDING_ENABLED=false
RERANK_ENABLED=false
RETRIEVAL_CANDIDATE_COUNT=10
```

### Balanced Retrieval

```env
EMBEDDING_ENABLED=true
EMBEDDING_TOP_K=15
RERANK_ENABLED=true
RERANK_TOP_K=8
RETRIEVAL_CANDIDATE_COUNT=25
```

### Local Private Deployment

```env
LLM_URL=http://host.docker.internal:8000/v1/chat/completions
LLM_KEY=
LLM_MODEL=local-chat-model

EMBEDDING_URL=http://host.docker.internal:8001/v1/embeddings
EMBEDDING_MODEL=local-embedding-model
EMBEDDING_API_KEY=

RERANK_URL=http://host.docker.internal:8002/rerank
RERANK_MODEL=local-reranker-model
RERANK_API_KEY=
```

## Security Notes

Do not commit real `.env` files.

Commit only `.env.example` with placeholders such as:

```env
LLM_KEY=your_api_key
```

Before publishing, check for:

- API keys
- private domains
- internal IP addresses
- personal model names
- logs
- backup files
