import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from ffmpeg_filtergraph_builder.core import build_vertical_reframe_graph, build_voice_ducking_graph


class TestFfmpegFiltergraphBuilder(unittest.TestCase):
    def test_vertical_reframe_graph_structure(self) -> None:
        g = build_vertical_reframe_graph(1080, 1920, 24)
        self.assertIn("[0:v]split=outputs=2[bg_src][fg_src]", g)
        self.assertIn("gblur=sigma=24[bg_blur]", g)
        self.assertTrue(g.endswith("[v_out]"))

    def test_voice_ducking_graph_structure(self) -> None:
        g = build_voice_ducking_graph(-14.0)
        self.assertIn("loudnorm=I=-14.0:TP=-1.5:LRA=11[vo_norm]", g)
        self.assertIn("sidechaincompress=", g)
        self.assertTrue(g.endswith("[a_out]"))


if __name__ == "__main__":
    unittest.main()
