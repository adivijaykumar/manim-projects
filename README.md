# Manim Projects

Manim animations for gravitational-wave physics outreach and talks.

| Project | Description |
|---|---|
| [`bh_globular_cluster/`](bh_globular_cluster/) | Black hole merger hierarchy in a globular cluster — mass segregation through repeated mergers |
| [`gw241011_boson_stars/`](gw241011_boson_stars/) | GW241011's spin-induced quadrupole moment and what it rules out for boson stars |

Each project directory is self-contained: its own scene file, `render_and_combine.sh`, and README with quick-start instructions.

## Prerequisites

- [Manim Community](https://docs.manim.community/en/stable/installation.html) (`pip install manim`)
- FFmpeg (bundled with most Manim installs; or `brew install ffmpeg`)
- LaTeX (for math labels — `brew install --cask mactex` on macOS)

If you use conda, create an env once:

```bash
conda create -n manim_env python=3.11
conda activate manim_env
pip install manim
```

Each project's render script auto-detects a `manim_env` conda environment if found; otherwise it falls back to whichever `manim` is on your PATH.
