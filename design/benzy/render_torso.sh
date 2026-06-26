#!/usr/bin/env bash
# Render the torso curation set from benzy_torso.scad (openscad + xvfb, headless).
set -euo pipefail
cd "$(dirname "$0")"
OUT=renders; mkdir -p "$OUT"
SCAD=benzy_torso.scad
COMMON="--imgsize=1000,1000 --colorscheme=Tomorrow"
r(){ local name=$1 v=$2 show=$3 cam=$4; shift 4
  xvfb-run -a openscad -o "$OUT/$name.png" -D "VARIANT=$v" -D "SHOW=\"$show\"" \
    --camera="$cam" --projection=perspective $COMMON "$@" "$SCAD" 2>/dev/null
  echo "  $name.png"; }

echo "Variants — front 3/4 (face/chin/charging side):"
r torso_v1_front 1 solid 0,0,0,72,0,205,285
r torso_v2_front 2 solid 0,0,0,72,0,205,285
r torso_v3_front 3 solid 0,0,0,72,0,205,285
echo "Variants — rear 3/4 (backpack/exhaust side):"
r torso_v1_rear 1 solid 0,0,0,72,0,25,285
r torso_v2_rear 2 solid 0,0,0,72,0,25,285
r torso_v3_rear 3 solid 0,0,0,72,0,25,285
echo "Interface map (v1, color-coded zones):"
r torso_interfaces 1 interfaces 0,0,0,70,0,205,295
echo "Section cutaway (v3, interior: SoM/heatpipe/speaker/battery):"
r torso_section 3 section 0,0,0,72,0,205,300
echo "done."
