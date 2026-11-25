# Changelog

All notable changes to `ffmpeg-filtergraph-builder` are documented in this file.

## [1.0.0] - 2026-11-25

### Added
- Composable `FilterGraph` builder emitting deterministic `[in]filter=k=v[out]` chains.
- Pre-built recipes for `9:16` vertical blurred-backdrop reframing, EBU R128 `-14 LUFS` loudness normalization, and `sidechaincompress` voiceover music ducking.
- CLI (`ffgraph`) and GitHub Actions CI matrix.
