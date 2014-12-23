#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import math

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: circle.py N")
        exit(1)
    n = int(sys.argv[1])
    for k in range(n):
        print str(math.cos(2*math.pi*k/n)) + " " + str(math.sin(2*math.pi*k/n))
