#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
algos_pip.py : Ensemble de programmes permettant de savoir si un point 
est contenu dans un polygone.
"""


def crossing_number(polygon, point):
    absc, ordo = point.coordinates
    points = polygon.points
    x_coord, y_coord = zip(*[point.coordinates for point in points])
    nombre_de_points = len(points)
    nombre_impair_de_noeuds = False

    j = nombre_de_points - 1

    for i in range(nombre_de_points):
        if y_coord[i] < ordo <= y_coord[j] or y_coord[j] < ordo <= y_coord[i]:
            if (
                x_coord[i]
                + (ordo - y_coord[i])
                / (y_coord[j] - y_coord[i])
                * (x_coord[j] - x_coord[i])
                < absc
            ):
                nombre_impair_de_noeuds = not nombre_impair_de_noeuds
        j = i

    return nombre_impair_de_noeuds


# élimination des calculs sur les segments à droite du point
def crossing_number_v2(polygon, point):
    absc, ordo = point.coordinates
    points = polygon.points
    x_coord, y_coord = zip(*[point.coordinates for point in points])
    nombre_de_points = len(points)
    nombre_impair_de_noeuds = False

    j = nombre_de_points - 1

    for i in range(nombre_de_points):
        if (
            y_coord[i] < ordo <= y_coord[j]
            or y_coord[j] < ordo <= y_coord[i]
            and (x_coord[i] <= absc or x_coord[j] <= absc)
        ):
            if (
                x_coord[i]
                + (ordo - y_coord[i])
                / (y_coord[j] - y_coord[i])
                * (x_coord[j] - x_coord[i])
                < absc
            ):
                nombre_impair_de_noeuds = not nombre_impair_de_noeuds
        j = i

    return nombre_impair_de_noeuds


def crossing_number_v3(polygon, point):
    absc, ordo = point.coordinates
    points = polygon.points
    x_coord, y_coord = zip(*[point.coordinates for point in points])
    nombre_de_points = len(points)
    nombre_impair_de_noeuds = False

    j = nombre_de_points - 1

    for i in range(nombre_de_points):
        if (
            y_coord[i] < ordo <= y_coord[j]
            or y_coord[j] < ordo <= y_coord[i]
            and (x_coord[i] <= absc or x_coord[j] <= absc)
        ):
            # xor plus rapide que ^=
            nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (
                not x_coord[i]
                + (ordo - y_coord[i])
                / (y_coord[j] - y_coord[i])
                * (x_coord[j] - x_coord[i])
                < absc
            )
        j = i

    return nombre_impair_de_noeuds


def crossing_number_v3_sec(polygon, point):
    absc, ordo = point.coordinates
    points = polygon.points
    indice = 0
    nombre_de_points = len(points)
    sommet0 = points[-1].coordinates
    ecart0 = sommet0[1] - ordo
    nombre_impair_de_noeuds = False

    while indice < nombre_de_points:
        sommet1 = points[indice].coordinates
        ecart1 = sommet1[1] - ordo
        if ecart0 * ecart1 > 0 or ecart0 == ecart1 == 0:
            sommet0 = sommet1
            indice += 1
            continue
        if (sommet1[0] <= absc or sommet0[0] <= absc) and (
            sommet0[1] >= ordo > sommet1[1] or sommet1[1] >= ordo > sommet0[1]
        ):
            nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (
                not sommet1[0]
                + (ordo - sommet1[1])
                / (sommet0[1] - sommet1[1])
                * (sommet0[0] - sommet1[0])
                < absc
            )
        ecart0 = ecart1
        sommet0 = sommet1
        indice += 1

    return nombre_impair_de_noeuds


# tri des segments, on peut break lsq l'on passe à droite du point
def crossing_number_v3_segments(polygon, point):
    absc, ordo = point.coordinates
    segments = sorted(list(polygon.segments()))
    indice = 0
    nombre_de_points = len(segments)
    nombre_impair_de_noeuds = False

    while indice < nombre_de_points:
        segment = segments[indice].endpoints
        sommet0 = segment[0].coordinates
        ecart0 = sommet0[1] - ordo
        sommet1 = segment[1].coordinates
        ecart1 = sommet1[1] - ordo
        if sommet1[0] > absc and sommet0[0] > absc:
            break
        if ecart0 * ecart1 > 0 or ecart0 == ecart1 == 0:
            sommet0 = sommet1
            indice += 1
            continue
        if sommet0[1] >= ordo > sommet1[1] or sommet1[1] >= ordo > sommet0[1]:
            # xor plus rapide que ^=
            nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (
                not sommet1[0]
                + (ordo - sommet1[1])
                / (sommet0[1] - sommet1[1])
                * (sommet0[0] - sommet1[0])
                < absc
            )
        indice += 1

    return nombre_impair_de_noeuds


# on évite la division
def crossing_number_v5(polygon, point):
    absc, ordo = point.coordinates
    points = polygon.points
    sommet0 = points[-1].coordinates
    y0_test = sommet0[1] >= ordo
    indice = 0
    nombre_impair_de_noeuds = False

    while indice < len(points):
        sommet1 = points[indice].coordinates
        y1_test = sommet1[1] >= ordo
        if y0_test != y1_test:
            nombre_impair_de_noeuds = (not nombre_impair_de_noeuds) != (
                not (
                    (sommet1[1] - ordo) * (sommet0[0] - sommet1[0])
                    >= (sommet1[0] - absc) * (sommet0[1] - sommet1[1])
                )
                == y1_test
            )
        y0_test = y1_test
        sommet0 = sommet1
        indice += 1

    return nombre_impair_de_noeuds


def left_line(p0, p1, p2):
    """Renvoie si un point est à gauche/sur/à droite d'une ligne (pas un segment hein)
    Return: > 0 pour p2 à gauche de la ligne (p0, p1)
            = 0 pour p2 sur cette ligne
            < 0 pour p2 à sa droite
    """
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


def winding_number(polygon, point):
    """http://geomalgorithms.com/a03-_inclusion.html"""
    absc, ordo = point.coordinates
    points = polygon.points
    indice = 0
    nombre_de_points = len(points)
    sommet0 = points[-1].coordinates
    nombre_impair_de_noeuds = 0

    while indice < nombre_de_points:
        sommet1 = points[indice].coordinates
        if sommet0[1] <= ordo:  # start y <= ordo
            if sommet1[1] > ordo:  # an upward crossing
                if left_line(sommet0, sommet1, [absc, ordo]) > 0:  # P left of edge
                    nombre_impair_de_noeuds += 1  # have a valid up intersect
        else:  # start y > ordo (no test needed)
            if sommet1[1] <= ordo:  # a downward crossing
                if left_line(sommet0, sommet1, [absc, ordo]) < 0:  # P right of edge
                    nombre_impair_de_noeuds -= 1  # have a valid down intersect
        sommet0 = sommet1
        indice += 1

    return nombre_impair_de_noeuds
