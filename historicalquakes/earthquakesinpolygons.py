from shapely.geometry import Polygon, Point
import numpy as np

# writes a new file of all beachballs in a polygon
# ONLY WANT SHALLOW (<70KM) EARTHQUAKES - USE THIS ONE
# arguments - the polygon coordinates as a list, new name to write the beachballs to
# returns the centre of the polygon, needed for Kostrov summation 
def coordinates(n):
    infile = open("allpolygons-polygons.txt")

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

def shallow_is_inside(file_name):
    # opening focal mechanism data - want to open the converted version of beachballs
    # this is all the beachballs, asking the question is each ball in the polygon
    newfile = open("%s" % file_name, "w")

    for i in range(1, 22):
        infile = open("gmthistearthquakes.txt")
        counter = 0
        coords = coordinates(i)

        newfile.write("##########   POLYGON%i    ##########\n" % i)
        # using Shapely to make Polygon
        poly = Polygon(coords)

        # middle of Polygon
        centre_point = np.array(poly.centroid.coords)


        # starts reading the data to work out if each focal is in polygon
        for line in infile:
            if counter == 0:
                counter += 1
                continue

            words = line.split() 
            
            # finding depth - if deeper than 70km we don't want it
            depth = float(words[4])

            if depth > 70:
                continue

            # taking longitude and latitude
            long = float(words[3])
            lat = float(words[2])

            # using Shapely to make it a Point
            point = Point(long, lat)

            # is this focal mechanism in my polygon?
            contains = point.within(poly)

            # if it is inside the polygon, write it in a new file
            if contains == True:
                newfile.write(line)
                newfile.write("\n")
        newfile.write("\n")
        infile.close()

    # returns centre_point because need it for Kostrov summation      
    return centre_point

shallow_is_inside("all_earths_polygons.txt")