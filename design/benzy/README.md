# Benzy — parametric CAD (OpenSCAD)

Component-modular massing model of **Benzy (Vector 3.0)**, the **canonical** machine
(no arms, no drone — per the render brief's honesty line). Built for curation: each part is a
separate module and there are three silhouette styles to compare.

## Render
```bash
sudo apt-get install -y openscad xvfb     # headless raster render
./render.sh                               # writes PNGs + an STL into ./renders/
```

## Curate via overrides
```bash
openscad -o out.png -D 'STYLE=2' -D 'SHOW="head"' --camera=0,0,110,62,0,205,150 benzy.scad
```
- **STYLE** — `1` Heritage (curvy, Vector-evolved) · `2` Rugged (chunky, big tracks) · `3` Sleek (tall, smooth, slim tracks)
- **SHOW** — `all` · `head` · `base` · `torso` · `internals` (x-ray placement) · `exploded` · `dock`
- **HEAD_TILT** — gaze angle (deg)
- Per-style proportions live in the `styles` table at the top of `benzy.scad` — edit one row to tune a variant.

## Components (separate modules, assemble later)
`drive_base()` (tracks + body + beltline) · `torso()` (+ backpack bay) · `head()` (face plate, convex
lens, eyes, camera bar, mic ring) · `internals()` (battery / RK3588S SoM / STM32 / fan placement) ·
`dock()` (cradle + LiDAR puck + contacts). `shell_all()` = base+torso+head.

## Notes
- Massing/proportion study — not yet a printable assembly (parts are separate solids).
- Camera z-rotation `205` faces the front (the face on +Y). `25` would show the rear.
- Dimensions track the spec (~105×80×130 mm). Once a direction is curated, the winner gets
  modeled properly in **SketchUp** (assembly structure + styled render) and refined toward real parts.
