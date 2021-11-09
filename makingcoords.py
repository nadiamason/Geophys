import numpy as np
# a program to convert kml files to longitude and latitude coords
"""KML has cordinates [Long, Lat, Alt, ' ', Long, Lat, Alt, ' '] 
we don't care about altitude, so we want to remove them and also the space
Ideally aim is to finish this file with a list of 
[(175, -30), (185, -30), (185, -43), (175, -43)] format
a list, with arrays of (long, lat) """

# kmlfile name is area-polygons.kml
# newtxtfile name is to be area-polygons.txt
def kmltotxt(kmlfile, newtxtfile):
    infile = open("%s" % (kmlfile))
    newfile = open("%s" % (newtxtfile), "w")
    counter = 0
    for line in infile:
        words = line.split()
        firstword = words[0]
        if firstword[0] == "<":
            continue
        counter += 1
        polygon = []

        for i in words:
            list_numbers = i.split(",")
            altitude = list_numbers.pop(2)
            polygon.append(list_numbers)
        
        newfile.write(str(polygon))
        newfile.write("\n")

kmltotxt("northview-polygons.kml", "northview-polygons.txt")
        