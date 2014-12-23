#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import cmath
import math
import os


def read_points(file_name):
    points = []
    with open(file_name, "r") as input_file:
        for line in input_file.readlines():
            x, y = line.split(" ")
            points.append(complex(float(x), float(y)))
    return points


def invert_points_1(points, epsilon):
    inverted_points = []
    for point in points:
        inverted_points.append(1 / ((1 + epsilon)*point))
    return inverted_points


def transform_points(points):
    with open("fftpts.dat", "w") as output_file:
        for point in points:
            output_file.write(str(point.real) + " " + str(point.imag) + "\n")
    os.system("echo \"0\nfftpts.dat\nfftpts.img\n0\" | ./forward")
    transformed_points = []
    with open("fftpts.img", "r") as input_file:
        for line in input_file.readlines():
            x, y = float(line[0:25]), float(line[25:])
            transformed_points.append(complex(x, y))
    os.system("rm fftpts.dat")
    os.system("rm fftpts.img")
    return transformed_points


def invert_points_2(points, shift):
    inverted_points = []
    for point in points:
        inverted_points.append(1 / point + shift)
    return inverted_points


def write_points(file_name, points):
    with open(file_name, "w") as output_file:
        for point in points:
            output_file.write(str(point.real) + " " + str(point.imag) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: apply_phi.py DAT_FILE_NAME PTS_FILE_NAME SHIFT_X SHIFT_Y EPSILON")
        exit(1)
    dat_file_name = sys.argv[1]
    pts_file_name = sys.argv[2] 
    shift = complex(float(sys.argv[3]), float(sys.argv[4]))
    epsilon = float(sys.argv[5])
    points = read_points(dat_file_name)

    inverted_points = invert_points_1(points, epsilon)
    transformed_points = transform_points(inverted_points)
    inverted_transformed_points = invert_points_2(transformed_points, shift)

    write_points(pts_file_name, inverted_transformed_points)
