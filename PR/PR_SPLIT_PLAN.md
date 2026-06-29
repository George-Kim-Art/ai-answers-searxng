# Suggested PR Split

This change can be submitted as one PR, but it will be easier to review if split into smaller PRs.

## PR 1: Documentation and Docker Examples

Include:

- `README.md`
- `docs/*`
- `examples/*`
- `.gitignore`
- `CHANGELOG.md`

Purpose:

- Explain the architecture.
- Document supported providers.
- Add safe deployment templates.
- Let maintainers review the direction before reviewing code.

## PR 2: Dynamic Model Resolver

Include:

- `plugins/model_resolver.py`
- minimal integration in `plugins/ai_answers.py`
- relevant docs updates

Purpose:

- Add fixed/auto model mode.
- Support OpenAI-compatible `/v1/models` discovery.
- Keep fallback behavior safe.

## PR 3: Semantic Retrieval and Rerank

Include:

- `plugins/semantic_rank.py`
- retrieval integration in `plugins/ai_answers.py`
- configuration docs updates

Purpose:

- Add optional embedding ranking.
- Add optional rerank support.
- Preserve fail-open behavior.

## Why split?

- Smaller diffs are easier to review.
- Maintainers can discuss the architecture early.
- Optional features can be accepted independently.
