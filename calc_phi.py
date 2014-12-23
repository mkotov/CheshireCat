#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import BeautifulSoup
import cmath
import math
import os

def read_points_from_svg(file_name, path_n):
    with open(file_name, "r") as input_file:
        content = input_file.read()
    soup = BeautifulSoup.BeautifulSoup(content)
    path = soup.findAll("path")[path_n]
    data = path.get("d").split(" ")
    x, y = 0, 0
    is_move_to = False
    is_relative = False
    points = []
    for d in data:
        if d == "m":
            is_move_to = True
            is_relative = True
        elif d == "M":
            is_move_to = True
            is_relative = False
        elif d == "z":
            pass
        elif d == "Z":
            pass
        elif d == "l":
            is_move_to = False
            is_relative = True
        elif d == "L":
            is_move_to = False
            is_relative = False
        else:
            dx, dy = d.split(",")
            dx = float(dx)
            dy = float(dy)
            if is_move_to:
                x = dx
                y = dy
                is_move_to = False
            else:
                if is_relative:
                    x += dx
                    y += dy
                else:
                    x = dx
                    y = dy
            points.append(complex(x, y))
    return points


def invert_points(points, shift):
    inverted_points = []
    for point in points:
        inverted_points.append(1 / (point - shift))
    return inverted_points


def calc_phi(points):
    with open("init.dat", "w") as output_file:
        for point in points:
            output_file.write(str(point.real) + " " + str(point.imag) + "\n")
        output_file.write("\n0.0 0.0\n")
    os.system("echo \"init.dat\n200\npoly.dat\" | ./polygon")
    os.system("./zipper")
    os.system("rm init.dat")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: calc_phi.py SVG_FILE_NAME PATH_N SHIFT_X SHIFT_Y")
        exit(1)
    svg_file_name = sys.argv[1]
    path_n = int(sys.argv[2])
    shift = complex(float(sys.argv[3]), float(sys.argv[4]))
    points = read_points_from_svg(svg_file_name, path_n)
    inverted_points = invert_points(points, shift)
    calc_phi(inverted_points)
