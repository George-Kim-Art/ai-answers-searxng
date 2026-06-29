# AI Answers for SearXNG

AI Answers adds LLM-powered answers to SearXNG search results.

This version keeps the original plugin behavior and adds optional modular extensions:

- OpenAI-compatible LLM backends
- Optional semantic retrieval with embeddings
- Optional reranking
- Dynamic model discovery
- Modular provider-neutral helper files
- Docker deployment examples

All new retrieval and model-discovery features are opt-in. If no new environment variables are configured, the plugin works like the original fixed-model setup.

## Project Layout

```text
plugins/
├── ai_answers.py          # Main SearXNG plugin entrypoint
├── semantic_rank.py       # Embedding + rerank retrieval helper
├── model_resolver.py      # Fixed / auto model resolver
└── __init__.py

docs/
├── INSTALL.md             # Manual installation
├── DOCKER.md              # Docker one-click deployment guide
├── CONFIGURATION.md       # Full environment variable reference
├── PROVIDERS.md           # Supported LLM, embedding and rerank providers
├── ARCHITECTURE.md        # Runtime architecture and extension points
├── UPGRADE.md             # Upgrade and migration guide
├── DEVELOPMENT.md         # Notes for future maintainers
└── FAQ.md

examples/
├── docker/                # Generic Docker template
├── openai/                # OpenAI hosted API template
├── ollama/                # Local Ollama / OpenAI-compatible gateway template
├── oneapi/                # OneAPI / NewAPI template
├── litellm/               # LiteLLM gateway template
└── vllm/                  # vLLM OpenAI-compatible server template
```

## Quick Start with Docker

```bash
cd examples/docker
cp .env.example .env
# edit .env and set your LLM endpoint and API key

docker compose up -d
```

Open SearXNG and enable/use the AI Answers plugin according to your SearXNG configuration.

See [docs/DOCKER.md](docs/DOCKER.md) for the full Docker guide.

## Manual Installation

Copy the plugin files into your SearXNG plugin directory:

```text
plugins/
├── ai_answers.py
├── semantic_rank.py
└── model_resolver.py
```

Then enable the plugin in your SearXNG settings.

See [docs/INSTALL.md](docs/INSTALL.md).

## Supported Backends

The plugin is designed around OpenAI-compatible APIs.

Common LLM backends:

- OpenAI
- Ollama OpenAI-compatible API
- vLLM
- LiteLLM
- OneAPI
- NewAPI
- SiliconFlow
- Local OpenAI-compatible gateways

Embedding backends:

- OpenAI-compatible embeddings API
- Ollama embeddings through a compatible gateway
- vLLM / TEI / LiteLLM / OneAPI / NewAPI style endpoints where compatible

Rerank backends:

- TEI rerank endpoint
- Jina AI rerank API
- Cohere-compatible rerank API

See [docs/PROVIDERS.md](docs/PROVIDERS.md).

## Configuration

The most important variables are:

```env
LLM_PROVIDER=openai
LLM_URL=https://api.openai.com/v1/chat/completions
LLM_KEY=your_api_key
LLM_MODEL=gpt-4o-mini

EMBEDDING_ENABLED=false
RERANK_ENABLED=false
```

Full reference: [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

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
    │              selected LLM model
    │
    ├──────────────► semantic_rank.py
    │                    │
    │                    ├─ optional embedding ranking
    │                    └─ optional reranking
    │
    ▼
Prompt Builder
    │
    ▼
LLM Response
```

Full architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Contributing / PR Notes

For upstream review, keep changes modular:

1. Documentation and Docker examples
2. Dynamic model resolver
3. Semantic retrieval and rerank pipeline

See [PR_SPLIT_PLAN.md](PR_SPLIT_PLAN.md).
