from shapely.geometry import Point, Polygon, polygon
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# takes the number of the polygon (starting with polygon 1) returns coords as list needed
# ALSO NEEDS TO CONVERT NEGATIVE COORDINATES!!!!
# arguments - takes number of poly and areaname
# returns - list of coords needed for shapely 
def coordinates():
    infile = open("allpolygons-polygons.txt" )

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

    return all_polygons         

# writes a new file of all beachballs in a polygon
# ONLY WANT SHALLOW (<70KM) EARTHQUAKES - USE THIS ONE
# arguments - the polygon coordinates as a list, new name to write the beachballs to
# returns the centre of the polygon, needed for Kostrov summation 
def shallow_is_inside(coords, file_name):
    # opening focal mechanism data - want to open the converted version of beachballs
    # this is all the beachballs, asking the question is each ball in the polygon
    infile = open("convertedstrainrates.txt")
    newfile = open("%s" % file_name, "w")
    counter = 1

    for i in coords:
        strainxx_list = []
        strainyy_list = []
        infile = open("convertedstrainrates.txt")
        newfile.write("START OF POLYGON %i" % counter)
        newfile.write("\n")

        # using Shapely to make Polygon
        poly = Polygon(i)

        # middle of Polygon
        centre_point = np.array(poly.centroid.coords)

        # starts reading the data to work out if each focal is in polygon
        for line in infile:

            words = line.split() 
            
            try:
               x = float(words[0])
            except:
                continue

            # taking longitude and latitude
            long = float(words[1])
            lat = float(words[0])

            # using Shapely to make it a Point
            point = Point(long, lat)

            # is this focal mechanism in my polygon?
            contains = point.within(poly)

            # if it is inside the polygon, write it in a new file
            if contains == True:
                strainxx_list.append(float(words[2]))
                strainyy_list.append(float(words[3]))
                newfile.write(line)
        x, y = str(centre_point[0][0]), str(centre_point[0][1])
        avg_xx = str(   (sum(strainxx_list)/len(strainxx_list)) * 10**-9    )
        avg_yy = str(   (sum(strainyy_list)/len(strainyy_list)) *10**-9    )
        newfile.write("####  ")
        newfile.write("Average data:  ")
        line = [x, y, avg_xx, avg_yy]
        [str(x) for x in line]
        [newfile.write("%s  " % x) for x in line]
        newfile.write("\n")
        counter += 1     
    return centre_point
list_polygons = coordinates()

shallow_is_inside(list_polygons, "strainsinpolygons.txt",)