# FAQ

## Does this change the default behavior?

No. Semantic retrieval, reranking, and dynamic model discovery are disabled unless explicitly configured.

## Do I need embeddings?

No. Embeddings are optional. Without embeddings, the plugin uses the normal SearXNG result order.

## Do I need a reranker?

No. Reranking is optional. It is most useful when search results contain many similar or noisy documents.

## Can I use local models?

Yes, if your local gateway exposes OpenAI-compatible chat, embeddings, or model-list endpoints.

## What is the difference between embedding and reranking?

Embedding ranking compares the query and documents in vector space to find semantically related results. Reranking then reorders the selected candidates with a model optimized for relevance scoring.

## What happens if the embedding or rerank API fails?

The plugin logs the failure and falls back to the original result order.

## What happens if dynamic model discovery fails?

The plugin falls back to `LLM_MODEL_FALLBACK` or `LLM_MODEL`.

## Are API keys required?

Only if the selected provider requires them. Local endpoints may not require keys.
