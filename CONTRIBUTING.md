# Contributing to ffmpeg-filtergraph-builder

1. Fork and clone the repository.
2. Add unit tests in `tests/` verifying rendered `[pad]` wiring for any new filtergraph recipe.
3. Run `python -m unittest discover -s tests -v` before opening a pull request.
