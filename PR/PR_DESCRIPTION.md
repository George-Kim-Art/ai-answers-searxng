## Summary

This PR adds optional, modular enhancements to AI Answers while preserving the existing behavior by default.

## What changed

- Added `semantic_rank.py` for optional embedding retrieval and reranking.
- Added `model_resolver.py` for fixed or automatic model selection.
- Kept `ai_answers.py` as the main orchestration layer.
- Added detailed documentation for installation, Docker, configuration, providers, architecture, upgrades and maintenance.
- Added safe Docker examples for multiple OpenAI-compatible backends.

## Design goals

- Preserve backward compatibility.
- Keep new features opt-in.
- Avoid provider-specific SDK dependencies.
- Support OpenAI-compatible LLM and embedding APIs.
- Keep optional retrieval failures from breaking normal search.
- Make the architecture easier for future contributors to modify.

## Default behavior

With default configuration:

```env
LLM_MODEL_MODE=fixed
EMBEDDING_ENABLED=false
RERANK_ENABLED=false
```

The plugin uses the configured fixed model and does not call embedding or rerank endpoints.

## Documentation added

- `docs/INSTALL.md`
- `docs/DOCKER.md`
- `docs/CONFIGURATION.md`
- `docs/PROVIDERS.md`
- `docs/ARCHITECTURE.md`
- `docs/UPGRADE.md`
- `docs/DEVELOPMENT.md`
- `docs/FAQ.md`

## Docker examples added

- `examples/docker`
- `examples/openai`
- `examples/ollama`
- `examples/oneapi`
- `examples/litellm`
- `examples/vllm`

All examples use placeholders only and do not include private configuration.
