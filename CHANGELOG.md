# Changelog

## Unreleased

### Added

- Optional semantic retrieval pipeline
- Optional rerank pipeline
- Dynamic model resolver
- Modular helper files for retrieval and model discovery
- Documentation for installation, architecture, configuration, providers, upgrade, and FAQ

### Changed

- Context selection can now use optional embedding and rerank stages when enabled.
- Model selection can now use fixed mode or automatic model discovery.

### Compatibility

- Existing behavior is preserved by default.
- New features are disabled unless configured through environment variables.
