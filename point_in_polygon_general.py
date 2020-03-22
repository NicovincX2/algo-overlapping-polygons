import sys
from pprint import pprint
from tycat import read_instance, read_instance_v3
from itertools import combinations, islice, cycle
from collections import Counter, defaultdict, OrderedDict
from operator import itemgetter


def couples(iterable):
    """
    iterate on all couples of given iterable.
    this will wrap around last element.
    """
    return zip(iterable, islice(cycle(iterable), 1, None))

def absolute_area(polygone):
    return abs(sum(cross_product(p1, p2) for p1, p2 in couples(polygone)) / 2)

def cross_product(p1, p2):
    return -p1[1] * p2[0] + p1[0] * p2[1]

def crossing_number_global(segments, ordo, max_x, results):#, poly_number, number_couples):
    """Renvoie si le point est dans le polygone.

    Si le point est exactement sur le bord du polygone, cette fonction peut retourner True ou False.

    Parameters:
        polygon (Polygon): //
        point (Point): //

    Returns:
        boolean : True if point in polygon

    """
    d = []

    for poly_indice, points in segments:
        # après affectation results[poly_number] = indice
        # lsq ligne indice, il ne faut pas prendre les segments de poly_number
        for result in results:
            if result == poly_indice:
                continue
        # (value[0], poly_indice)
        # if (poly_number, poly_indice) not in number_couples:
        #     continue
        # print(poly_indice, points)
        counter = 0
        nombre_de_points = len(points)
        sommet0 = points[-1]
        while counter < nombre_de_points:
            #segment = segments[indice]
            #sommet0 = segment[1][0]
            sommet1 = points[counter]
            # test de hauteur
            #if (sommet0[1] >= ordo > sommet1[1] or sommet1[1] >= ordo > sommet0[1]): # and (sommet1[0] <= absc or sommet0[0] <= absc):
            if (sommet0[1] >= ordo > sommet1[1] or sommet1[1] >= ordo > sommet0[1]):# and (sommet1[0] <= max_x or sommet0[0] <= max_x): # la deuxième condition apporte un petit gain
                # le membre de gauche est la coordonnée de l'intersection du segment
                # avec la droite y
                inter = sommet1[0] + (ordo - sommet1[1]) / (sommet0[1] - sommet1[1]) * (sommet0[0] - sommet1[0])
                #if (sommet1[0] <= inter or sommet0[0] <= inter):
                # if inter < absc:
                #     # print("intersection")
                # poly = ligne[0]
                # segment_numero_poly = segment[0]
                # if inter < max_x:
                # if poly != segment_numero_poly: # on ne compte pas les intersections avec d'autres segments du même polygone
                print("Polygone avec intersection :", poly_indice)
                d.append((poly_indice, inter))
            sommet0 = sommet1
            counter += 1

    return sorted(d, key=lambda couple: couple[1]) # nécessaire


def get_segments(polygones):
    # les segments du fichier des polygones sont déjà triés
    # ie. points d'un même polygone à la suite des autres
    # on a besoin de trier car on enlève des éléments ensuite
    segments = []
    # poly_indices = []
    # dictionnaire ce clé y et de valeur les points sur y
    y_points = defaultdict(list)
    for indice, polygon in polygones:
        # print(compteur)
        # poly_indices.append(indice)
        points = []
        for segment in polygon.segments():
            # segment_coord = []
            # points = segment.endpoints
            # for point in points:
            #     coord = point.coordinates
            #     segment_coord.append(coord)
            # first_point = points[0].coordinates
            # # on a besoin que du premier point
            # #segments.append((indice, sorted(segment_coord, key=lambda p: p[1])))
            # segments.append((indice, segment_coord))
            # en fait on a besoin que du premier point
            first_point = segment.endpoints[0].coordinates
            #segments[indice].append(first_point)
            points.append(first_point)
            # on ne veut pas de polygones en doublons
            for value in y_points[first_point[1]]:
                if value[0] == indice:
                    break
            else:
                y_points[first_point[1]].append((indice, first_point[0]))
        segments.append((indice, points))

    return segments, y_points

def choose_y(y_points, nombre_polygones):
    y_points_needed = defaultdict(list)
    poly_found = set()
    # on ne garde que les lignes avec le plus de points
    # on veut tous les polygones
    for ligne, value in sorted(y_points.items(), key=lambda x: len(x[1]), reverse=True):
        # print(ligne, value)
        # poly_indices, point = zip(*value)
        if len(poly_found) == nombre_polygones:
            break
        for indice, point in value:
            if indice not in poly_found:
                # poly_found.update(set(poly_indices))
                poly_found.add(indice)
                # print(poly_found)
                y_points_needed[ligne].append((indice, point))
    return y_points_needed

def trouve_inclusions_general(polygones):
    """problème avec 1
    ligne qui passe par 3 sommets (2 polygones carré gauche et grand milieu)

    """

    ### TEST des QUADRANTS ###
    #quadrants = [polygon.bounding_quadrant() for polygon in polygones]
    # on ne test pas les autres polygones
    sorted_polygones = sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area)
    #poly_indices, _ = zip(*sorted_polygones)
    #number_couples = set(combinations(poly_indices, 2)) # attention, combinations renvoie un générateur

    # print(number_couples)
    # for indice_poly1, indice_poly2 in number_couples:
    #     if not quadrants[indice_poly1].intersect_2(quadrants[indice_poly2]):
    #         continue

    nombre_polygones = len(polygones)
    results = [-1] * nombre_polygones
    # get all segments
    segments, y_points = get_segments(sorted_polygones)

    # segments.sort(key=lambda couple: couple[1][0][1]) # tri selon les y croissants
    # pprint(y_points)
    # print(len(y_points))

    # for indice, polygon in enumerate(polygones):
    #     # poly_indices.append(indice)
    #     segments_polygon = list(couples(polygon))
    #     # segments.extend(segments_polygon) # on a pas l'indice
    #     for segment in segments_polygon:
    #         segments.append((indice, segment))
    #     for segment in segments_polygon:
    #         first_point = segment[0]
    #         # on ne veut pas de polygones en doublons
    #         for value in y_points[first_point[1]]:
    #             if value[0] == indice:
    #                 break
    #         else:
    #             y_points[first_point[1]].append((indice, first_point[0]))


    # pprint(y_points)
    pprint(segments)
    nombre_segments = len(segments)
    y_points_needed = choose_y(y_points, nombre_polygones)
    pprint(y_points_needed)
    # print(len(y_points_needed))

    for ligne, value in y_points_needed.items():
        print(f"y = {ligne}")
        max_x = max(value, key=itemgetter(1))[1]
        # print(max_x)
        # pprint(segments)
        liste_intersections = crossing_number_global(segments, ligne, max_x, results)#, value, number_couples)
        if not liste_intersections: continue
        pprint(liste_intersections)
        for poly_number, abscisse in value:
        # for poly_number, abscisse in value:
        #     liste_intersections = crossing_number_global(segments, ligne, max_x, poly_number, number_couples)
            #print(poly_number)
            polygones_a_tester = []
            for count, (indice_poly, liste_segments) in enumerate(segments):
                # print(indice_poly, count)
                if count == nombre_segments - 1:
                    break
                if indice_poly == poly_number:
                    polygones_a_tester, _ = zip(*segments[count + 1:])
                    break
            if not polygones_a_tester: break

            pprint(polygones_a_tester)
            #liste_intersections = crossing_number_global(segment_a_tester, ligne, max_x)
            #pprint(liste_intersections)
            print(f"may be in polygone {poly_number}")
            #less_inter = [couple for couple in liste_intersections if couple[0] in polygones_a_tester and couple[1] < abscisse]# and (poly_number, couple[0]) in number_couples]
            #if not less_inter: continue
            #print(f"Intersections de segments avec {poly_number} sur y = {ligne}")
            #pprint(less_inter)
            #count = Counter(couple[0] for couple in less_inter)
            count = Counter(couple[0] for couple in liste_intersections if couple[0] in polygones_a_tester and couple[1] < abscisse)
            # on ne retest pas ERREUR
            # for poly_numb in polygones_a_tester:
            # del segments[poly_number]
            for indice, intersection_number in count.items():
                # if (poly_number, indice) not in number_couples: # nécessaire
                #     continue
                ### TEST des QUADRANTS ### trop long
                # if not quadrants[indice].intersect_2(quadrants[poly_number]):
                #     continue

                if intersection_number % 2 == 1:
                    print(f"Polygone {poly_number} in {indice}")
                    # lsq ligne indice, il ne faut pas prendre les segments de poly_number
                    results[poly_number] = indice
    return results


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        # polygones = read_instance_v3(fichier)
        inclusions = trouve_inclusions_general(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
