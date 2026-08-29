# Black Hole Merger Hierarchy

Manim animations visualizing how stellar-mass black holes in globular clusters undergo hierarchical mergers — from mass segregation through repeated gravitational-wave-emitting coalescences.

## Animations

| Scene class | Description |
|---|---|
| `MassSegregation` | Heavy objects sink to the cluster core; light ones drift to the edges |
| `EqualMassRatioMergers` | Two 1G black holes merge inside the dense core → 2G remnant with spin χ ≈ 0.7 |
| `SecondGenerationBH_v2` | The 2G black hole (2M, χ ≈ 0.7) merges with a 1G black hole → 3G remnant |

## Quick start

### Render everything (720p + 1080p, all scenes combined)

```bash
./render_and_combine.sh
```

### Render a single scene (preview quality)

```bash
manim -pql bh_globular_cluster.py MassSegregation
```

Replace `MassSegregation` with any scene class name. The `-p` flag opens the video after rendering.

### Render options

| Flag | Quality |
|---|---|
| `-ql` | 480p15 (fast preview) |
| `-qm` | 720p30 |
| `-qh` | 1080p60 |

```bash
# 720p only
./render_and_combine.sh -q m

# 1080p only
./render_and_combine.sh -q h

# Single scene at all qualities
./render_and_combine.sh -s EqualMassRatioMergers
```

Output lands in `media/videos/bh_globular_cluster/`.

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

The render script auto-detects a `manim_env` conda environment and uses it if found; otherwise it falls back to whichever `manim` is on your PATH.

## Project structure

```
.
├── bh_globular_cluster.py   # all scene classes
├── render_and_combine.sh    # render + ffmpeg combine helper
└── media/                   # generated output (git-ignored)
    └── videos/
        └── bh_globular_cluster/
            ├── 720p30/
            ├── 1080p60/
            └── black_hole_hierarchy_combined_*.mp4
```

## Adding new scenes

1. Add a new `class MyScene(Scene)` to `bh_globular_cluster.py`.
2. Render it:
   ```bash
   manim -pqh bh_globular_cluster.py MyScene
   ```
3. To include it in the combined video, add its name to the `SCENES` list in `render_and_combine.sh` (the default `SCENES` variable near the top of the script).
