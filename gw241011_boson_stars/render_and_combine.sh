#!/bin/bash

# Render and combine all scenes for the GW241011 boson star illustration.
# Usage:
#   ./render_and_combine.sh              # render all scenes at 720p and 1080p
#   ./render_and_combine.sh -q m         # 720p only
#   ./render_and_combine.sh -q h         # 1080p only
#   ./render_and_combine.sh -s GW241011Overview   # single scene, all qualities

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_FILE="$SCRIPT_DIR/gw241011_boson_stars.py"
OUTPUT_DIR="$SCRIPT_DIR/media/videos/gw241011_boson_stars"

QUALITY=""
SINGLE_SCENE=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -q|--quality) QUALITY="$2"; shift ;;
        -s|--scene)   SINGLE_SCENE="$2"; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

SCENES="${SINGLE_SCENE:-GW241011Overview SpinInducedQuadrupole RepulsiveBosonStarsExcluded SolitonicStarsAllowed ClosingSummary}"
QUALITIES="${QUALITY:-m h}"

MANIM_CMD="manim"
if command -v conda &> /dev/null && conda env list | grep -q manim_env; then
    MANIM_CMD="conda run -n manim_env manim"
fi

FFMPEG_CMD="ffmpeg"
if command -v conda &> /dev/null && conda env list | grep -q manim_env; then
    FFMPEG_CMD="conda run -n manim_env ffmpeg"
fi

echo "======================================"
echo " GW241011 Boson Star Animation Render"
echo "======================================"

for Q in $QUALITIES; do
    case $Q in
        m) LABEL="720p30"  ;;
        h) LABEL="1080p60" ;;
        l) LABEL="480p15"  ;;
        *) echo "Unknown quality: $Q (use l/m/h)"; exit 1 ;;
    esac

    echo ""
    echo "--- Rendering quality: -q$Q ($LABEL) ---"
    $MANIM_CMD --disable_caching -q$Q "$PYTHON_FILE" $SCENES

    if [[ -z "$SINGLE_SCENE" ]]; then
        CONCAT_FILE="/tmp/concat_gw241011_${LABEL}.txt"
        printf "" > "$CONCAT_FILE"
        for SCENE in $SCENES; do
            echo "file '$OUTPUT_DIR/$LABEL/${SCENE}.mp4'" >> "$CONCAT_FILE"
        done

        COMBINED="$OUTPUT_DIR/gw241011_boson_stars_combined_${LABEL}.mp4"
        echo "Combining into $COMBINED ..."
        $FFMPEG_CMD -f concat -safe 0 -i "$CONCAT_FILE" -c copy "$COMBINED" -y
        rm -f "$CONCAT_FILE"
        echo "Combined output: $COMBINED"
    fi
done

echo ""
echo "======================================"
echo " Done!"
echo "======================================"
