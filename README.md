# ffmpeg-filtergraph-builder

[![CI](https://github.com/tarikra1/ffmpeg-filtergraph-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/tarikra1/ffmpeg-filtergraph-builder/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/release-v1.0.0-0EA5E9.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Composable, zero-dependency Python `-filter_complex` builder for `9:16` vertical reframing, EBU R128 `-14 LUFS` loudness normalization, and `sidechaincompress` voiceover ducking.**

## Quickstart

```bash
pip install -e .
ffgraph vertical-reframe --width 1080 --height 1920
ffgraph voice-duck --lufs -14.0
```

## License

MIT License — see [LICENSE](LICENSE).
