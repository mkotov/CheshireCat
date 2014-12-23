#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from PIL import Image, ImageDraw
import cmath
import math

def draw_points(image, points):
    draw = ImageDraw.Draw(image)
    for ends in zip(points, points[1:] + [points[0]]):
        draw.line(((ends[0].real, ends[0].imag), (ends[1].real, ends[1].imag)))
    for point in points:
        r = 2
        draw.ellipse((point.real - r, point.imag - r, point.real + r, point.imag + r), fill="green")


def get_value(points, z, radius):
    result = 1
    for point in points:
        result *= (z - point) / radius
    return z * (1 + result)


def get_radius(points):
    n = len(points)
    result = 0
    for k in range(n):
        result += points[k] * cmath.exp(-2j*math.pi*k/n)
    return result / n


def draw_fractal(image, points, scale, shift, bound, max_num_iter, radius):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    percents = -1
    for y in range(0, height):
        new_percents = round(100.0 * y / height)
        if new_percents != percents:
            percents = new_percents
            print(str(percents) + " %")
        for x in range(0, width):
            try:
                z = (complex(x, y) - shift) * scale
                n = 0
                while abs(z) < bound and n < max_num_iter:
                    z = get_value(points, z, radius)
                    n += 1
                if n < max_num_iter:
                    color = ((100 * n) % 255, 128 + (50 * n) % 255, 128 + (75 * n) % 255)
                    draw.point((x, y), color)
            except KeyboardInterrupt:
                return
            except:
                pass

def read_points(file_name):
    points = []
    with open(file_name, "r") as input_file:
        for line in input_file.readlines():
            x, y = line.split(" ")
            points += [complex(float(x), float(y))]
    return points


def transform_points(points, scale, shift):
    transformed_points = []
    for point in points:
        transformed_points.append(scale * (point - shift))
    return transformed_points


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: points_to_fractal.py PTS_FILE_NAME WIDTH HEIGHT SCALE SHIFT_X SHIFT_Y BOUND MAX_ITER")
        exit(1)
    pts_file_name = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    scale = float(sys.argv[4])
    shift = complex(float(sys.argv[5]), float(sys.argv[6]))
    bound = float(sys.argv[7])
    max_num_iter = int(sys.argv[8])
    points = read_points(pts_file_name)
    transformed_points = transform_points(points, scale, shift)
    result_image = Image.new("RGBA", (width, height))
    radius = get_radius(transformed_points)
    draw_fractal(result_image, transformed_points, scale, shift, bound, max_num_iter, radius)
#    draw_points(result_image, points)
    result_image.show()
