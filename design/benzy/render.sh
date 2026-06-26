#!/usr/bin/env bash
# Render the Benzy curation set (PNGs + an STL) from benzy.scad.
# Needs: openscad + xvfb (headless). Outputs to ./renders/.
set -euo pipefail
cd "$(dirname "$0")"
OUT=renders; mkdir -p "$OUT"
SCAD=benzy.scad
COMMON="--imgsize=1000,1100 --colorscheme=Tomorrow"

r(){ # name STYLE SHOW camera [extra...]
  local name=$1 st=$2 show=$3 cam=$4; shift 4
  xvfb-run -a openscad -o "$OUT/$name.png" -D "STYLE=$st" -D "SHOW=\"$show\"" \
    --camera="$cam" --projection=perspective $COMMON "$@" "$SCAD" 2>/dev/null
  echo "  $name.png"
}

echo "Silhouette variants (3 styles):"
r benzy_style1_iso 1 all 0,0,65,60,0,205,440
r benzy_style2_iso 2 all 0,0,65,60,0,205,470
r benzy_style3_iso 3 all 0,0,65,60,0,205,440

echo "Components (style 1):"
r benzy_head       1 head      0,0,110,62,0,205,150
r benzy_base       1 base      0,0,24,62,0,202,300
r benzy_torso      1 torso     0,0,69,62,0,205,230
r benzy_internals  1 internals 0,0,65,62,0,205,460
r benzy_exploded   1 exploded  0,0,95,60,0,205,640
r benzy_dock       1 dock      0,0,20,60,0,205,360

echo "Ortho front (style 1):"
xvfb-run -a openscad -o "$OUT/benzy_front_ortho.png" -D "STYLE=1" -D 'SHOW="all"' \
  --camera=0,0,65,90,0,180,400 --projection=ortho $COMMON "$SCAD" 2>/dev/null
echo "  benzy_front_ortho.png"

echo "STL (style 1 assembly):"
openscad -o "$OUT/benzy_style1.stl" -D "STYLE=1" -D 'SHOW="all"' "$SCAD" 2>/dev/null
echo "  benzy_style1.stl"
echo "done."
