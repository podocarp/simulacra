## Helmholtz

[contour](img/contour.png)

Simulates a Helmholtz coil with an optional magnetic dipole in the middle.
Configure through editing the `.py` file.

## Usage

It is simple and dirty.

`python helmholtz.py contour` plots the 2D contour at a cross section at y=0.

`python helmholtz.py field` plots the full 3D field.

`python helmholtz.py all` plots both of them

The 2D plots still calculate the whole 3D field before drawing. This is honestly
inefficient but it still works reasonably fine `div = 100` (so 1000000 points),
runs in a few seconds.

You won't be able to pull it off with the 3D plot though, the default `div = 10`
works just fine for visualization. The reason is the 3D projection runs on CPU
(I think) and takes ages. Furthermore the exported `.svg` is completely unusable
due to the amount of data points.
