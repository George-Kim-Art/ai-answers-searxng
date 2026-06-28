## Summary

This PR adds optional semantic retrieval, optional reranking, and dynamic model discovery to AI Answers while preserving the existing behavior by default.

## What changed

- Added `semantic_rank.py` for embedding-based context selection and optional reranking
- Added `model_resolver.py` for fixed or auto model resolution
- Updated `ai_answers.py` to use the helper modules when configured
- Added documentation for installation, architecture, configuration, retrieval providers, upgrade, and FAQ

## Design goals

- Keep the original plugin behavior unchanged unless new options are enabled
- Keep provider-specific retrieval logic outside the main plugin file
- Support OpenAI-compatible embedding providers and common rerank API styles
- Make the architecture easier to understand and extend

## Supported retrieval APIs

Embedding:

- OpenAI-compatible embeddings API
- Gateways such as vLLM, LiteLLM, OneAPI/NewAPI, and similar services when they expose compatible embeddings endpoints

Rerank:

- TEI style
- Jina style
- Cohere-compatible style

## Compatibility

All new features are opt-in.

If users do not set `EMBEDDING_ENABLED`, `RERANK_ENABLED`, or `LLM_MODEL_MODE=auto`, the plugin should continue to behave like the original implementation.
