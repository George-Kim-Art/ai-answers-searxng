# Architecture

The plugin is split into three main files.

```text
plugins/
├── ai_answers.py
├── semantic_rank.py
└── model_resolver.py
```

## Runtime flow

```text
User Query
    │
    ▼
SearXNG Search Results
    │
    ▼
ai_answers.py
    │
    ├── resolves model through model_resolver.py
    │
    ├── optionally ranks context through semantic_rank.py
    │
    ├── builds prompt
    │
    └── streams LLM answer
```

## ai_answers.py

Main responsibilities:

- Receive the user query
- Collect SearXNG results
- Select context
- Build the prompt
- Call the configured LLM provider
- Render the answer in the result page

The default behavior remains unchanged when optional retrieval features are disabled.

## semantic_rank.py

Main responsibilities:

- Build retrieval candidates from search results
- Call an embedding endpoint when enabled
- Rank candidates by vector similarity
- Call a reranker endpoint when enabled
- Return the selected context back to `ai_answers.py`

The module is optional at runtime. If retrieval is not configured, it returns the original result order.

## model_resolver.py

Main responsibilities:

- Use a fixed configured model by default
- Optionally discover the active model from a `/v1/models` endpoint
- Cache model discovery results
- Fall back to the configured model when discovery fails

## Compatibility model

All new features are controlled by environment variables. Existing deployments do not need to change configuration.
