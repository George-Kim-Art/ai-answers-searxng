# AI Answers for SearXNG

This branch keeps the original AI Answers plugin behavior while adding optional, modular retrieval features.

## Highlights

- Optional semantic retrieval using OpenAI-compatible embedding APIs
- Optional reranking using TEI, Jina, or Cohere-compatible rerank APIs
- Optional dynamic model discovery for OpenAI-compatible model gateways
- Modular helper files: `semantic_rank.py` and `model_resolver.py`
- Backward compatible defaults: if no new environment variables are set, the plugin behaves like the original version

## Architecture

```text
User Query
    │
    ▼
ai_answers.py
    │
    ├──────────────► model_resolver.py
    │                    │
    │                    ▼
    │             Current LLM model
    │
    └──────────────► semantic_rank.py
                         │
                         ▼
                  Embedding ranking
                         │
                         ▼
                  Optional reranking
                         │
                         ▼
                    Selected context

Selected context + model
    │
    ▼
Prompt builder
    │
    ▼
LLM response
```

`ai_answers.py` remains the orchestration layer. Provider-specific retrieval and model-selection logic lives in helper modules so the main plugin remains easier to maintain.

## Supported Embedding Providers

Any provider exposing an OpenAI-compatible embeddings endpoint should work.

| Provider / Gateway | Support |
| --- | --- |
| OpenAI-compatible APIs | Supported |
| vLLM | Supported through OpenAI-compatible API |
| LiteLLM | Supported through OpenAI-compatible API |
| OneAPI / NewAPI | Supported through OpenAI-compatible API |
| Ollama-compatible gateways | Supported if embeddings endpoint is OpenAI-compatible |
| SiliconFlow-style gateways | Supported if embeddings endpoint is OpenAI-compatible |
| Jina embeddings | Supported if endpoint returns OpenAI-style embedding data |

## Supported Rerank Providers

| Provider / API style | Support |
| --- | --- |
| TEI reranker | Supported |
| Jina reranker | Supported |
| Cohere-compatible rerank API | Supported |

## Documentation

- [Installation](docs/INSTALL.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Configuration](docs/CONFIGURATION.md)
- [Retrieval providers](docs/PROVIDERS.md)
- [Upgrade guide](docs/UPGRADE.md)
- [FAQ](docs/FAQ.md)

## Design Goal

All new capabilities are opt-in. A user can install the plugin exactly as before and ignore semantic retrieval, reranking, and model discovery unless they explicitly configure them.

## Docker deployment

A generic Docker Compose example is available in:

- `examples/docker/docker-compose.yml`
- `examples/docker/.env.example`
- `docs/DOCKER.md`

The example uses safe placeholders only. Copy `.env.example` to `.env`, fill in
your own endpoints and keys, then start the stack with Docker Compose.
