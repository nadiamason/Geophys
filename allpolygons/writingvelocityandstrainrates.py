from pyproj import Geod
from shapely.geometry import Polygon
import numpy as np
import math

def makingpolygon(n, areaname):
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
    polygon_coords = all_polygons[n-1] 
  
    poly = Polygon(polygon_coords)
    return poly

def convert(degminsec):
    letter = degminsec[-1]

    if letter == "N":
        multiplier = 1
    elif letter == "S":
        multiplier = 1
    else:
        multiplier = -1

    numbers = enumerate(degminsec[:-1].split('-'))

    answer = sum(float(x) / 60 ** n for n, x in numbers)

    return multiplier * answer

def total_m0s(m0polygonfile):
    # finding sum of scalar moments in area
    secondfile = open(m0polygonfile, "r")
    scalar_moment_list = []

    for line in secondfile:
        bits = line.split()
        m0 = float(bits[-1])
        m0 = m0 / 10**7
        scalar_moment_list.append(m0)
    
    return sum(scalar_moment_list)

def readingpoints(number):
    infile = open("points.kml")
    #for line in infile:
     #   if line[:9] == "\t\t\t<name>":
      #      if line[9] == number:
    data = []
 
    [data.append(line) for line in infile]

    counter = 0
    length = len(data)
    longitudes = []
    latitudes = []
    while counter < length:
        line = data[counter]
        if line[:9] == "\t\t\t<name>":
            point_number = line[line.find('>')+1:line.rfind('<')]
            if point_number == str(number):
                longitude = data[counter + 2]
                latitude = data[counter + 3]

                long = longitude[longitude.find('>')+1:longitude.rfind('<')]
                lat = longitude[longitude.find('>')+1:longitude.rfind('<')]

                longitudes.append(long)
                latitudes.append(lat)
        counter += 1
            
    return longitudes, latitudes
                






            


areaname = "allpolygons"
total_polys = int(input("how many polygons?  "))
newfile = open("velocityandstrain.csv", "w")


headers = "polygon number, surface area, depth, volume, mu, length, dip in degrees, dip in rads, w, catalogue length, big eigen, small eigen, strainrateone, strainratetwo, velocity"
newfile.write(headers)
newfile.write("\n")

Geod = Geod(ellps = 'WGS84')
for i in range(1,total_polys + 1):

    # polygon number
    dataline = []
    dataline.append(i)

    # Surface area
    poly = makingpolygon(i, areaname = "allpolygons")
    area = (Geod.geometry_area_perimeter(poly)[0])
    dataline.append(area)

    # depth
    depth = float(input("What is the seismogenic depth for polygon number %i? " % i))
    dataline.append(depth)

    # volume
    volume = area * depth
    dataline.append(volume)

    # mu - rigidity
    mu = 3.3e10
    dataline.append(mu)

    # length
    longitudes, latitudes = readingpoints(i)
    long1 = longitudes[0]
    long2 = longitudes[1]
    lat1 = latitudes[0]
    lat2 = latitudes[1]
    
    azimuth1, azimuth2, distance = Geod.inv(long1, lat1, long2, lat2)
    dataline.append(distance)

    # dip from mttk
    dip_degrees = float(input("What is the dip for polygon %i? (from mttk) "  % i))
    dip_radians = np.deg2rad(dip_degrees)
    dataline.append(dip_degrees)
    dataline.append(dip_radians)

    # trig for w
    w = depth / np.sin(dip_radians)
    dataline.append(w)


    # catalogue length, tau
    tau = float(input("what is catalogue length? "))
    dataline.append(tau)
    
    largesteigen = float(input("What is the largest eigen value? "))
    dataline.append(largesteigen)
    smallesteigen = float(input("What is the smallest eigen value? "))
    dataline.append(smallesteigen)
    denominator = 1 / (2 * mu * volume * tau)
    strainrateone = denominator * largesteigen
    dataline.append(strainrateone)
    strainratetwo = denominator * smallesteigen
    dataline.append(strainratetwo)

    # VELOCITIES
    m0 = total_m0s("m0%spolygon%i.txt" % (areaname, i))
    first_term = 1 / (mu * distance * w * tau)
    velocity = first_term * m0
    dataline.append(velocity)


    lineasstrings = [str(x) for x in dataline]
    finalline = ','.join(lineasstrings)

    newfile.write(finalline)
    newfile.write("\n")