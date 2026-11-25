"""CLI for ffmpeg-filtergraph-builder."""

from __future__ import annotations

import argparse

from .core import build_vertical_reframe_graph, build_voice_ducking_graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ffgraph", description="Generate composable FFmpeg -filter_complex graphs.")
    sub = parser.add_subparsers(dest="recipe", required=True)

    vr = sub.add_parser("vertical-reframe", help="Generate 16:9 -> 9:16 blurred backdrop filtergraph.")
    vr.add_argument("--width", type=int, default=1080)
    vr.add_argument("--height", type=int, default=1920)
    vr.add_argument("--sigma", type=int, default=28)

    dk = sub.add_parser("voice-duck", help="Generate EBU R128 voice loudnorm + sidechain music ducking graph.")
    dk.add_argument("--lufs", type=float, default=-14.0)

    args = parser.parse_args(argv)
    if args.recipe == "vertical-reframe":
        print(build_vertical_reframe_graph(args.width, args.height, args.sigma))
    else:
        print(build_voice_ducking_graph(args.lufs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
