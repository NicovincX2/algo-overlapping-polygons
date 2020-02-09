#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_point_in_polygon.py : //
"""

import config
import pytest


from tycat import read_instance
from utils import get_files_matching_ext
from point_in_polygon import crossing_number, crossing_number_v2, crossing_number_v3, crossing_number_v4, crossing_number_v5
from geo.polygon import Polygon
from geo.point import Point


TESTS_2_POLY = [(crossing_number, "10x10.poly", True)]
POLY_FILES = get_files_matching_ext(".poly", ["generated.poly"] + [f"generated_from_examples_{i}.poly" for i in range(4, 8)])
POINT_IN_POLYGON_FUNCTIONS = (crossing_number_v5, crossing_number, crossing_number_v2, crossing_number_v3, crossing_number_v4)


@pytest.mark.parametrize("function", POINT_IN_POLYGON_FUNCTIONS)
def test_point_in_polygon_vertex_on_threshold(function):
    polygone, point = (Polygon([Point([0, 0]), Point([1, 1]), Point([2, 0]), Point([2, -2]), Point([1, -1]), Point([0, -2])]), Point([1, 0]))
    assert function(polygone, point) == True


@pytest.mark.parametrize("function", POINT_IN_POLYGON_FUNCTIONS)
def test_point_in_polygon_side_on_threshold(function):
    polygone, point = (Polygon([Point([0, 0]), Point([1, 0]), Point([2, 1]), Point([3, 0]), Point([2, -2]), Point([0, -2])]), Point([2, 0]))
    assert function(polygone, point) == True


@pytest.mark.parametrize("function", POINT_IN_POLYGON_FUNCTIONS)
def test_point_in_polygon_upper_triangles(function):
    polygone, point = (Polygon([Point([-1, 0]), Point([0, 1]), Point([1, 0]), Point([2, 1]), Point([3, 0]), Point([2, -2]), Point([0, -2])]), Point([2, 0]))
    assert function(polygone, point) == True


@pytest.mark.parametrize("function, file, expected", TESTS_2_POLY)
def test_point_in_polygon(function, expected, file):
    """on vérifie qu'un point du polygone est inclut dans l'autre polygone"""
    polygones = read_instance(file)
    assert len(polygones) == 2
    assert function(polygones[0], polygones[1].points[0]) == expected


@pytest.mark.parametrize("function, file, expected", TESTS_2_POLY)
def test_all_points_in_polygon(function, expected, file):
    """on vérifie que tous les points du polygone sont inclus dans l'autre polygone"""
    polygones = read_instance(file)
    assert len(polygones) == 2
    for point in polygones[1].points:
        assert function(polygones[0], point) == expected


@pytest.mark.parametrize("file", POLY_FILES)
def test_compare_functions(file, functions=POINT_IN_POLYGON_FUNCTIONS):
    polygones = read_instance(file)
    assert all(
        [
            function1(polygones[0], polygones[1].points[0]) == function2(polygones[0], polygones[1].points[0])
            for function1, function2 in zip(functions, functions[1:])
        ]
    )
