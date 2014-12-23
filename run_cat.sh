#!/bin/bash

python calc_phi.py cat.svg 0 320 240
python circle.py 200 > circle.dat
python apply_phi.py circle.dat result.pts 320 240 0.005
python draw_fractal.py result.pts 640 480 0.0001 320 240 100 15

rm -f *.dat *.img *.par *.pre *.pts
