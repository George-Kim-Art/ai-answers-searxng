# Changelog

## Unreleased

### Added

- Modular semantic retrieval helper: `plugins/semantic_rank.py`.
- Modular model resolver helper: `plugins/model_resolver.py`.
- Optional embedding-based ranking.
- Optional reranker support.
- Fixed and automatic model selection modes.
- Docker deployment examples for generic, OpenAI, Ollama, OneAPI/NewAPI, LiteLLM and vLLM deployments.
- Detailed documentation for installation, Docker deployment, configuration, providers, architecture, upgrade and maintenance.

### Compatibility

- Default behavior remains fixed-model mode.
- Embedding retrieval is disabled unless `EMBEDDING_ENABLED=true`.
- Rerank is disabled unless `RERANK_ENABLED=true`.
- Model auto-discovery is disabled unless `LLM_MODEL_MODE=auto`.

### Security

- Real `.env` files are ignored.
- Example files use placeholders only.
- Local deployment details, private URLs and API keys are not included.
