# GW241011 & Rotating Exotic Compact Objects

Manim animations illustrating "Implications of GW241011 for rotating exotic compact objects"
(N. V. Krishnendu et al., arXiv:[2511.17341](https://arxiv.org/abs/2511.17341), Phys. Rev. Lett.,
DOI [10.1103/29y5-nx9y](https://journals.aps.org/prl/abstract/10.1103/29y5-nx9y)) — GW241011's
asymmetric masses and rapidly-spinning primary give the tightest constraint yet on the
spin-induced quadrupole moment, ruling out repulsive boson stars entirely and requiring any
surviving exotic alternative to be nearly as compact as a black hole.

## Animations

| Scene class | Description |
|---|---|
| `GW241011Overview` | The event itself: very unequal masses ($q\approx0.30$), primary spin $\chi_1\approx0.78$ |
| `SpinInducedQuadrupole` | What $\kappa$ is, why a mismatched signal would reveal it, and the measured constraint |
| `RepulsiveBosonStarsExcluded` | $\kappa$–$\chi$ exclusion for repulsive boson stars, across every coupling |
| `SolitonicStarsAllowed` | Solitonic/axionic boson stars that survive weak enough coupling |
| `ClosingSummary` | One-sentence wrap-up: every coupling/mass ruled out, survivors need $C\gtrsim0.24$ |

## Quick start

### Render everything (720p + 1080p, all scenes combined)

```bash
./render_and_combine.sh
```

### Render a single scene (preview quality)

```bash
manim -pql gw241011_boson_stars.py GW241011Overview
```

Replace with any scene class name above. The `-p` flag opens the video after rendering.

### Render options

| Flag | Quality |
|---|---|
| `-ql` | 480p15 (fast preview) |
| `-qm` | 720p30 |
| `-qh` | 1080p60 |

Output lands in `media/videos/gw241011_boson_stars/`.

## Data

`data/boson_stars/` mirrors the numerically-computed rotating boson star sequences (repulsive,
solitonic, axionic, mini potentials) from
[github.com/tamaraevst/Spin-induced-quadrupole-moments-of-boson-stars](https://github.com/tamaraevst/Spin-induced-quadrupole-moments-of-boson-stars),
the data release accompanying the paper above. Not currently used directly by the scenes (see
below) but kept for reference/future scenes; cite Krishnendu et al. 2025 and Siemonsen & East
2021 (arXiv:2011.08247) per that repo's README if reused.

`data/from_paper_figures/` holds data extracted directly from the paper's own published figures
(PDFs supplied by the author), rather than re-derived from the raw sequences above — the raw
sequences turned out to include unstable/non-physical branches that a naive spin-interpolation
picks up, so the published figures (already correctly filtered) are the source of truth here:

- `repulsive_curves.json`, `solitonic_axionic_efs_curves.json` — $(\chi,\kappa)$ points pulled
  from the vector paths inside the figure PDFs (matplotlib embeds the actual plotted line
  segments, so this recovers the real data points, not pixel positions), plus the measured
  $\kappa$–$\chi$ credible-region outline.
- `mass_coupling_regions.json` — boundary values for the excluded-region plot in the particle
  mass / self-interaction coupling plane, read off the same way. Not currently used by any
  scene (that plot was cut for pacing) but kept for a possible future scene.

## Notes on precision

- The $\kappa_1$ posterior in `SpinInducedQuadrupole` is an illustrative two-piece-normal
  distribution matching the paper's quoted median and 90% interval, not the actual posterior
  samples.
- `SolitonicStarsAllowed` plots only 4 of the 6 published solitonic couplings ($\sigma=0.04$,
  0.05, 0.08, 0.1) — the $\sigma=0.15,0.2$ curves had a stray path segment merged in during
  PDF extraction that produced a broken shape; they're not central to the "some boson stars
  survive" argument so were dropped rather than guessed at.
- The exotic-fluid-star family (third panel of the solitonic/axionic figure) isn't used —
  solitonic + axionic alone carry the "still allowed" story.

## Prerequisites

Same as the top-level project: [Manim Community](https://docs.manim.community/en/stable/installation.html),
FFmpeg, LaTeX. The render script auto-detects a `manim_env` conda environment if present.
