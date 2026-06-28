# Suggested PR Split

For easier review, this change can be submitted as separate PRs.

## PR 1: Documentation and architecture

Files:

```text
README.md
docs/INSTALL.md
docs/ARCHITECTURE.md
docs/CONFIGURATION.md
docs/PROVIDERS.md
docs/UPGRADE.md
docs/FAQ.md
CHANGELOG.md
```

Goal:

- Explain the proposed modular architecture
- Document configuration and provider compatibility
- Ask for maintainer feedback before merging larger code changes

## PR 2: Dynamic model resolver

Files:

```text
plugins/model_resolver.py
plugins/ai_answers.py
```

Goal:

- Add optional fixed/auto model resolution
- Keep fixed model mode as the default

## PR 3: Semantic retrieval and reranking

Files:

```text
plugins/semantic_rank.py
plugins/ai_answers.py
```

Goal:

- Add optional embedding ranking
- Add optional reranking
- Preserve original search result order when disabled
