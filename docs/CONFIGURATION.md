# Configuration

## Existing LLM configuration

| Variable | Description | Default |
| --- | --- | --- |
| `LLM_PROVIDER` | Provider preset name | empty |
| `LLM_URL` | Chat completion endpoint | provider default |
| `LLM_KEY` | LLM API key | empty |
| `LLM_MODEL` | Fixed model name | provider default |
| `LLM_MAX_TOKENS` | Maximum response tokens | `500` |
| `LLM_TEMPERATURE` | Sampling temperature | `0.2` |
| `LLM_CONTEXT_DEEP_COUNT` | Number of deep context results | `5` |
| `LLM_CONTEXT_SHALLOW_COUNT` | Number of shallow context results | `15` |
| `LLM_TABS` | Enabled SearXNG tabs | default plugin tabs |
| `LLM_INTERACTIVE` | Enable interactive UI | `true` |
| `LLM_QUESTION_MARK_REQUIRED` | Require question mark to trigger | `false` |

## Dynamic model resolver

| Variable | Description | Default |
| --- | --- | --- |
| `LLM_MODEL_MODE` | `fixed` or `auto` | `fixed` |
| `LLM_MODELS_URL` | OpenAI-compatible `/v1/models` endpoint | empty |
| `LLM_SWITCH_STATUS_URL` | Optional gateway status endpoint | empty |
| `LLM_MODEL_FALLBACK` | Fallback model if discovery fails | `LLM_MODEL` |
| `LLM_MODEL_CACHE_SECONDS` | Discovery cache TTL | `15` |
| `LLM_MODEL_DISCOVERY_TIMEOUT` | Discovery timeout in seconds | `5` |
| `LLM_MODEL_API_KEY` | API key for model discovery | `LLM_KEY` |
| `LLM_MODEL_API_KEY_HEADER` | Header name for model discovery auth | `Authorization` |
| `LLM_MODEL_API_KEY_SCHEME` | Header auth scheme | `Bearer` |
| `LLM_MODEL_VERIFY_SSL` | Verify SSL for model discovery | `true` |

## Semantic retrieval

| Variable | Description | Default |
| --- | --- | --- |
| `EMBEDDING_ENABLED` | Enable embedding ranking | `false` |
| `EMBEDDING_URL` | Embedding API endpoint | empty |
| `EMBEDDING_MODEL` | Embedding model name | empty |
| `EMBEDDING_API_KEY` | Embedding API key | empty |
| `EMBEDDING_API_FORMAT` | Embedding API format | `openai` |
| `EMBEDDING_TOP_K` | Number of embedding-ranked candidates | `15` |

## Reranker

| Variable | Description | Default |
| --- | --- | --- |
| `RERANK_ENABLED` | Enable reranking | `false` |
| `RERANK_URL` | Rerank API endpoint | empty |
| `RERANK_MODEL` | Rerank model name | empty |
| `RERANK_API_FORMAT` | `tei`, `jina`, or `cohere` | `tei` |
| `RERANK_TOP_K` | Number of reranked candidates | `8` |
| `RERANK_API_KEY` | Rerank API key | empty |
| `RERANK_API_KEY_HEADER` | Header name for rerank auth | `Authorization` |
| `RERANK_API_KEY_SCHEME` | Header auth scheme | `Bearer` |

## Shared retrieval options

| Variable | Description | Default |
| --- | --- | --- |
| `RETRIEVAL_CANDIDATE_COUNT` | Number of search results considered by retrieval | `25` |
| `RETRIEVAL_DOCUMENT_MAX_CHARS` | Max characters per document used for retrieval | `3000` |
| `RETRIEVAL_TIMEOUT` | Embedding/rerank request timeout | `10` |
| `RETRIEVAL_VERIFY_SSL` | Verify SSL for retrieval APIs | `true` |

## Example: OpenAI-compatible embedding API

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=https://your-gateway.example/v1/embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=your-key
```

## Example: TEI reranker

```env
RERANK_ENABLED=true
RERANK_URL=http://tei-reranker.example/rerank
RERANK_MODEL=BAAI/bge-reranker-large
RERANK_API_FORMAT=tei
```
