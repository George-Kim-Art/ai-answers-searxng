# Architecture

AI Answers is organized as a small modular plugin.

The main goal is to keep the original SearXNG plugin simple while isolating optional features into helper modules.

## High-Level Flow

```text
User query
    │
    ▼
SearXNG search
    │
    ▼
ai_answers.py
    │
    ├─────────────► model_resolver.py
    │                   │
    │                   ├─ fixed model mode
    │                   ├─ auto model discovery
    │                   └─ fallback model
    │
    ├─────────────► semantic_rank.py
    │                   │
    │                   ├─ candidate extraction
    │                   ├─ optional embedding ranking
    │                   └─ optional reranking
    │
    ▼
Prompt builder
    │
    ▼
LLM chat completions endpoint
    │
    ▼
AI answer shown in SearXNG
```

## `ai_answers.py`

This is the only file SearXNG loads as the plugin entrypoint.

It is responsible for:

- Reading environment variables.
- Integrating with the SearXNG plugin lifecycle.
- Receiving search results.
- Selecting candidate context.
- Calling `model_resolver.py` when model auto-discovery is enabled.
- Calling `semantic_rank.py` when embedding or rerank is enabled.
- Building the final LLM prompt.
- Calling the LLM endpoint.

It should not contain provider-specific retrieval code. Provider-specific logic belongs in helper modules.

## `model_resolver.py`

This module answers one question:

> Which model should the current request use?

Modes:

```text
fixed
  └─ always use LLM_MODEL

auto
  ├─ try LLM_SWITCH_STATUS_URL if configured
  ├─ try LLM_MODELS_URL if configured
  ├─ cache the discovered model
  └─ fall back to LLM_MODEL_FALLBACK or LLM_MODEL
```

Auto mode is useful when the LLM endpoint is a gateway that can switch models dynamically.

Examples:

- LiteLLM gateway
- OneAPI / NewAPI
- vLLM proxy
- custom OpenAI-compatible gateway

Failure behavior:

- If discovery fails, fixed fallback is used.
- Search should not fail because model discovery failed.

## `semantic_rank.py`

This module improves which search results are sent into the prompt.

Pipeline:

```text
Raw SearXNG results
    │
    ▼
Take top RETRIEVAL_CANDIDATE_COUNT
    │
    ▼
Extract title + URL + content snippet
    │
    ▼
If EMBEDDING_ENABLED=true:
    embed query and documents
    compute vector similarity
    keep EMBEDDING_TOP_K
    │
    ▼
If RERANK_ENABLED=true:
    send query + candidate documents to reranker
    keep RERANK_TOP_K
    │
    ▼
Return reordered context to ai_answers.py
```

Failure behavior:

- If embedding fails, original ranking is preserved.
- If rerank fails, embedding ranking or original ranking is preserved.
- Retrieval failure should not break SearXNG search.

## Why Use Helper Modules?

This structure makes maintenance easier:

- `ai_answers.py` remains readable.
- Retrieval providers can be added without touching prompt logic.
- Model discovery can evolve independently.
- Users can disable optional features with environment variables.
- Upstream maintainers can review each module separately.

## Extension Points

Future improvements can be added around these points:

### Before Prompt Construction

Add or reorder documents before the prompt is built.

Current implementation:

- embedding ranking
- reranking

Possible future extensions:

- domain filters
- freshness filters
- language-aware ranking
- duplicate URL removal

### Before LLM Call

Resolve model and request configuration.

Current implementation:

- fixed model
- auto model discovery

Possible future extensions:

- per-tab model selection
- per-query model routing
- cost-aware model selection

### After LLM Response

This project currently does not add post-processing hooks, but future maintainers could add:

- citation normalization
- answer quality checks
- safety filters
- response caching

## Backward Compatibility

Default behavior is conservative:

```env
LLM_MODEL_MODE=fixed
EMBEDDING_ENABLED=false
RERANK_ENABLED=false
```

With these defaults:

- No embedding endpoint is called.
- No rerank endpoint is called.
- No model discovery is required.
- The configured `LLM_MODEL` is used directly.
