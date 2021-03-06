from shapely.geometry import Point, Polygon
import numpy as np
import matplotlib.pyplot as plt


# takes the number of the polygon (starting with polygon 1) returns coords as list needed
# arguments - takes number of poly
# returns - list of coords needed for shapely 
def coordinates(n):
    infile = open("polygoncoords.txt")

    all_polygons = []

    for line in infile:
        words = line.replace(" ", "")
        words = words.strip()
        numbers = words.split("],[")
        numbers[0] = numbers[0].replace("[[",'')
        numbers[-1] = numbers[-1].replace("]]", '')

        floated_list = []

        for coords in numbers:
            coordinate_pair = []
            number = coords.split(",")
            for i in number:
                i = i.replace("'", "")
                i = float(i)
                coordinate_pair.append(i)
            floated_list.append(coordinate_pair)

        all_polygons.append(floated_list)
    n = int(n)
    return all_polygons[n-1]            
        
# writes a new file of all beachballs in a polygon
# arguments - the polygon coordinates as a list, new name to write the beachballs to
# returns the centre of the polygon, needed for Kostrov summation 
def shallow_is_inside(coords, file_name):
    # opening focal mechanism data
    infile = open("C:/Users/nadia/Documents/University/geophys project/convertedlong.txt")

    newfile = open("%s" % file_name, "w")

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

# Kostrov summation for polygon
# ONLY WANT SHALLOW (<70KM) EARTHQUAKES
# arguments - file of poly. data to sum, new file name to write data to, centre point of polygon
# returns list of mrr, mtt, mpp etc. for the summation
def Kostrov_summation(polygonname, filename, centre):
    # Kostrov summation code, takes mrr, mtt, mpp, mrt, mrp and mtp

    # open the focal file 
    infile = open("%s" % polygonname)

    # create a new file to write out mrr, mtt, mpp etc. values
    newfile = open("%s" % filename, "w")

    # setting empty lists
    mrr_list = []
    mtt_list = []
    mpp_list = []
    mrt_list = []
    mrp_list = []
    mtp_list = []

    # looping through mechanisms
    for line in infile:
        words = line.split()

        # iexp values
        power = float(words[9])

        # mrr values
        #mrr = (float(words[3]) * (10**(power - 7)))
        mrr = (float(words[3]) * (10**power))
        mrr_list.append(mrr)

        # mtt values
        #mtt = (float(words[4]) * (10**(power - 7)))
        mtt = (float(words[4]) * (10**power))
        mtt_list.append(mtt)

        # mpp values
        #mpp = (float(words[5]) * (10**(power - 7)))
        mpp = (float(words[5]) * (10**power))
        mpp_list.append(mpp)

        # mrt values
        #mrt = (float(words[6]) * (10**(power - 7)))
        mrt = (float(words[6]) * (10**power))
        mrt_list.append(mrt)

        # mrp values
        #mrp = (float(words[7]) * (10**(power - 7)))
        mrp = (float(words[7]) * (10**power))
        mrp_list.append(mrp)

        # mtp values
        #mtp = (float(words[8]) * (10**(power - 7)))
        mtp = (float(words[8]) * (10**power))
        mtp_list.append(mtp)

    mrr_total = sum(mrr_list)
    mtt_total = sum(mtt_list)
    mpp_total = sum(mpp_list)
    mrt_total = sum(mrt_list)
    mrp_total = sum(mrp_list)
    mtp_total = sum(mtp_list)

    totals = [mrr_total, mtt_total, mpp_total, mrt_total, mrp_total, mtp_total]

    # taking the longitude and latitude of the centre of the polygon
    longitude = centre[0][0]
    latitude = centre[0][1]

    # all values from summation
    line = [mrr_total, mtt_total, mpp_total, mrt_total, mrp_total, mtp_total]
    # turns into string
    lineasstrings = [str(x) for x in line]

    power_list = []
    for x in lineasstrings:
        # takes the last two numbers which is the power e.g. ...e+20
        power = x[-2:]
        # adds to list of all the powers
        power_list.append(power)
    
    # what is the largest power
    max_power = float(max(power_list))

    # divide by the largest power 
    line_array = np.array(line) / 10**max_power
    
    # change back to list from array
    line = line_array.tolist()

    # add my power to end of list as order needed for meca 
    line.append(max_power)
    
    # adding the longitude, latitude and 0 to start as needed for meca format
    to_insert = [longitude, latitude, 0] 
    line = to_insert + line

    # turning line into a list of strings so can join them
    lineasstrings = [str(x) for x in line]
    finalline = ' '.join(lineasstrings)

    newfile.write(finalline)

    return totals

# works out the seismic consistency of the area
# arguments - data from Kostrov with m0 added from linux, m0 beachball file
# returns seismic consistency value
def seismic_consistency(m0polygonfile, m0beachballfile):
    # finding scalar moment of sum tensor
    infile = open(m0polygonfile, "r")
    
    for line in infile:
        words = line.split()
        s_moment_average = float(words[-1])

    # finding sum of scalar moments in area
    secondfile = open(m0beachballfile, "r")
    scalar_moment_list = []

    for line in secondfile:
        bits = line.split()
        scalar_moment_list.append(float(bits[-1]))
        sum_scalar_moments = sum(scalar_moment_list)

    seis_consistency = s_moment_average/sum_scalar_moments

    return seis_consistency

# plots frequ-mag graph
# arguments - mw beach ball data
# shows the graph and returns the a, b values as [-b, a]
def frequ_mag_graph(mwbeachballs):
    # opening focal mechanism data with mw on the end
    infile = open(mwbeachballs)

    total_number = 0
    magnitudes = []

    for line in infile:
        total_number += 1
        words = line.split()
        mw = float(words[-1])
        magnitudes.append(mw)
    print("Total number is %f" % total_number)
    magn = 4.5
    list_mags = []
    frequencies = []
    logged_freq = []

    while magn <= 8:
        count = sum(mw >= magn for mw in magnitudes)
        frequencies.append(count)
        magn += 0.5

    try:
        while True:
            frequencies.remove(0)
    
    except ValueError:
        pass

    for freq in frequencies:
        freq = np.log10(freq)
        logged_freq.append(freq)

    magn = 4.5
    for log in logged_freq:
        list_mags.append(magn)
        magn += 0.5


    plt.yscale("log")
    # plotting the line 1 points 
    plt.scatter(list_mags, frequencies , c='k', label= "Actual Data")

    plt.ylim(None, 10**4)
    plt.xlim(4,None)

    p = np.polyfit(list_mags, logged_freq, 1)
    p1d = np.poly1d(p)
    a = round(p[1], 3)
    b = -1 * round(p[0], 3)
    plt.plot(list_mags, 10**p1d(list_mags), "g--", label = "Line of Best Fit  log10N = %.3f - %.3fM" % (a,b))


    plt.xlabel('Mw - magntiude')
    # Set the y axis label of the current axis.
    plt.ylabel('Number of Earthquakes')
    # Set a title of the current axes.
    plt.title('Frequency-magnitude plot - polygon %s' % (n))
    # show a legend on the plot
    plt.legend()
    # Display a figure.
    plt.show()

    return a, b, list_mags, frequencies, p1d

# works out the error using squared error
# arguements - takes function of best fit line, x data, y data
# returns the error
def sqr_error(p, xi, yi):
    # squared to take magnitude so don't cancel each other out
    diff2 = (p(xi)-yi)**2
    return diff2.sum()

# plots the frequ of depths, in 5 km intervals 
# arguments - takes name of beachballfile
# returns nothing, shows the graph 
def depth_distribution(beachballname):
    # opening focal mechanism data with mw on the end
    infile = open(beachballname)

    total_number = 0
    depths = []

    for line in infile:
        try:
            total_number += 1
            words = line.split()
            depth = float(words[2])
            depths.append(depth)

        except:
            continue
    
    depth_tracker = 0
    higher_depth_tracker = 5
    depth_frequ = []
    while depth_tracker <= max(depths):
        count = sum(dep >= depth_tracker and dep < higher_depth_tracker for dep in depths)
        depth_frequ.append(count)

        depth_tracker += 5
        higher_depth_tracker += 5

    list_depths = []
    depth = 0
    for dep in depth_frequ:
        list_depths.append(depth)
        depth += 5

    plt.scatter(list_depths, depth_frequ, s = 2)
    plt.grid(True)
    plt.show()
    
# for polygon number n, does Kostrov summation - ONLY FOR SHALLOW EARTHQUAKES
def Kostrovsum(n):
    # POLYGON n
    polygonn = coordinates(n)
    changing_polygon = shallow_is_inside(polygonn, "polygon%s.txt" % (n))
    Kostrov_summation("polygon%s.txt" % (n), "Kostrov%s.txt" % (n), changing_polygon)

# part 2, need m0 and mw data for these files
def graphs(n):
    """ Have to use remote desktop to add_m0 to Kostrov1 data
        The line is: add_m0 Kostrov1.txt > m0Kostrov1.txt
        
    Then for frequ mag graphs need mw data, same process
    but for poly files"""
    print("%s" % (n))
    print(seismic_consistency("m0Kostrov%s.txt" % (n), "polygon%s.txt" % (n)))

    a, b, x, y, p1d = frequ_mag_graph("mwpolygon%s.txt" % (n))

    # currently not returned or stored just code in case
    #error = sqr_error(p1d, x, np.log10(y))
    
    #depth_distribution("polygon%s.txt" % (n))


# PART 1 - NEED TO DO FOR NEW/CHANGED POLYGONS BEFORE PART 2
total_polys = 9
n = 1
while n <= total_polys:
    Kostrovsum("%s" % n)
    n += 1

# PART 2 - NEED TO DO FOR NEW/CHANGED POLYGONS BEFORE PART 2
n = 1
while n <= total_polys:
    graphs("%s" % n)
    n += 1




