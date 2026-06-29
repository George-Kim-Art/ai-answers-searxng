# FAQ

## Do I need embeddings?

No. Embeddings are optional.

Set:

```env
EMBEDDING_ENABLED=false
```

## Do I need rerank?

No. Rerank is optional.

Set:

```env
RERANK_ENABLED=false
```

## What is the safest default setup?

Use fixed model mode and disable retrieval:

```env
LLM_MODEL_MODE=fixed
EMBEDDING_ENABLED=false
RERANK_ENABLED=false
```

## What does semantic retrieval improve?

It helps the prompt builder select search results that are semantically closer to the user query, instead of relying only on the original search order.

This can improve answer quality when search results contain mixed or noisy content.

## What does rerank improve?

A reranker compares the query and candidate documents directly and can produce a better final ordering than embeddings alone.

A common pipeline is:

```text
Search results → embeddings → top candidates → reranker → prompt
```

## Why does the plugin fail open?

Search should not break just because an optional retrieval service is unavailable.

If embedding or rerank fails, the plugin falls back to the original ranking.

## Can I use Ollama?

Yes, if you use Ollama's OpenAI-compatible endpoint.

Example:

```env
LLM_URL=http://host.docker.internal:11434/v1/chat/completions
LLM_MODEL=llama3.1
LLM_KEY=
```

## Can I use OneAPI, NewAPI or LiteLLM?

Yes. Use their OpenAI-compatible endpoint.

Example:

```env
LLM_URL=http://host.docker.internal:3000/v1/chat/completions
LLM_KEY=your_gateway_key
```

## Can I use a local embedding model?

Yes, if it exposes an OpenAI-compatible embeddings endpoint.

```env
EMBEDDING_ENABLED=true
EMBEDDING_URL=http://host.docker.internal:8001/v1/embeddings
EMBEDDING_MODEL=your_embedding_model
```

## Why is `localhost` not working in Docker?

Inside the SearXNG container, `localhost` means the SearXNG container itself.

Use:

```text
host.docker.internal
```

or the Docker Compose service name.

## Should I commit `.env`?

No.

Commit only `.env.example`.

## Why are there multiple example directories?

Different users run different model backends.

The examples provide safe starting points for:

- OpenAI
- Ollama
- OneAPI / NewAPI
- LiteLLM
- vLLM
- generic OpenAI-compatible deployments

## How should I add a new backend template?

Create:

```text
examples/provider-name/
├── docker-compose.yml
├── .env.example
└── settings.yml.example
```

Then update:

- `README.md`
- `docs/DOCKER.md`
- `docs/PROVIDERS.md`
