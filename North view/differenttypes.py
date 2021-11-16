from shapely.geometry import Point, Polygon, polygon
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def coordinates(n, areaname):
    infile = open("%s" % ("%s-polygons.txt" % areaname))

    all_polygons = []

    for line in infile:
        words = line.replace(" ", "")
        words = words.strip()
        numbers = words.split("],[")
        numbers[0] = numbers[0].replace("[[",'')
        numbers[-1] = numbers[-1].replace("]]", '')

        floated_list = []

        for coords in numbers:
            counter = 0
            coordinate_pair = []
            number = coords.split(",")
            for i in number:
    
                i = i.replace("'", "")
                i = float(i)

                # if my longitude coordinate is negative, cross line, make e.g. -175 --> 185
                if i < 0 and counter == 0:
                    difference = 180 - abs(i)
                    i = 180 + difference

                coordinate_pair.append(i)
                counter += 1
            floated_list.append(coordinate_pair)

        all_polygons.append(floated_list)
    n = int(n)
    hi = all_polygons[n-1]
    return all_polygons[n-1]   
def shallow_is_inside(coords, file_name, type):
    # opening focal mechanism data - want to open the converted version of beachballs
    infile = open("C:/Users/nadia/GeophysProj/Geophysics-Project/%smwm0convertedlong.txt" % type)

    newfile = open("C:/Users/nadia/GeophysProj/Geophysics-Project/North view/%s" % file_name, "w")

    # using Shapely to make Polygon
    poly = Polygon(coords)

    # middle of Polygon
    centre_point = np.array(poly.centroid.coords)

    # starts reading the data to work out if each focal is in polygon
    for line in infile:

        words = line.split() 
        
        # finding depth - if deeper than 70km we don't want it
        depth = float(words[2])
        if depth > 70:
            continue

        # taking longitude and latitude
        long = float(words[0])
        lat = float(words[1])

        # using Shapely to make it a Point
        point = Point(long, lat)

        # is this focal mechanism in my polygon?
        contains = point.within(poly)

        # if it is inside the polygon, write it in a new file
        if contains == True:
            newfile.write(line)

    # returns centre_point because need it for Kostrov summation      
    return centre_point


def making_dif_type_polys(n, areaname, type):
    coords = coordinates(n, areaname)
    shallow_is_inside(coords, "%s%spolygon%i.txt" % (type, areaname, n), type )


area = "northview"
total_polys = 7
n = 1
while n <= total_polys:
    making_dif_type_polys(n, area, "ss")
    making_dif_type_polys(n, area, "thrust")
    making_dif_type_polys(n, area, "normal")
    n += 1
