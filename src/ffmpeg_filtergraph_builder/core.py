"""Composable, shell-safe FFmpeg -filter_complex builder for short-form video pipelines."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FilterNode:
    inputs: list[str]
    name: str
    params: dict[str, object] = field(default_factory=dict)
    outputs: list[str] = field(default_factory=list)

    def render(self) -> str:
        ins = "".join(f"[{i}]" for i in self.inputs)
        outs = "".join(f"[{o}]" for o in self.outputs)
        if not self.params:
            body = self.name
        else:
            kv = ":".join(f"{k}={v}" for k, v in self.params.items())
            body = f"{self.name}={kv}"
        return f"{ins}{body}{outs}"


class FilterGraph:
    def __init__(self) -> None:
        self.nodes: list[FilterNode] = []

    def add(self, inputs: list[str], name: str, params: dict[str, object] | None = None, outputs: list[str] | None = None) -> "FilterGraph":
        self.nodes.append(FilterNode(inputs, name, params or {}, outputs or []))
        return self

    def render(self) -> str:
        return ";".join(n.render() for n in self.nodes)


def build_vertical_reframe_graph(width: int = 1080, height: int = 1920, blur_sigma: int = 28) -> str:
    """Create a 9:16 blurred-backdrop + crisp foreground filtergraph from 16:9 input `[0:v]`."""
    fg = FilterGraph()
    fg.add(["0:v"], "split", {"outputs": 2}, ["bg_src", "fg_src"])
    fg.add(["bg_src"], "scale", {"w": width, "h": height, "force_original_aspect_ratio": "increase"}, ["bg_scaled"])
    fg.add(["bg_scaled"], "crop", {"w": width, "h": height}, ["bg_cropped"])
    fg.add(["bg_cropped"], "gblur", {"sigma": blur_sigma}, ["bg_blur"])
    fg.add(["fg_src"], "scale", {"w": width, "h": -2}, ["fg_scaled"])
    fg.add(["bg_blur", "fg_scaled"], "overlay", {"x": "(W-w)/2", "y": "(H-h)/2"}, ["v_out"])
    return fg.render()


def build_voice_ducking_graph(target_lufs: float = -14.0) -> str:
    """Normalize voiceover `[0:a]` to target LUFS and sidechain-duck music `[1:a]` into `[a_out]`."""
    fg = FilterGraph()
    fg.add(["0:a"], "loudnorm", {"I": target_lufs, "TP": -1.5, "LRA": 11}, ["vo_norm"])
    fg.add(["vo_norm"], "asplit", {"outputs": 2}, ["vo_main", "vo_sc"])
    fg.add(["1:a"], "volume", {"volume": "0.28"}, ["bgm_low"])
    fg.add(["bgm_low", "vo_sc"], "sidechaincompress", {"threshold": 0.03, "ratio": 6, "attack": 15, "release": 280}, ["bgm_ducked"])
    fg.add(["vo_main", "bgm_ducked"], "amix", {"inputs": 2, "duration": "first"}, ["a_out"])
    return fg.render()
