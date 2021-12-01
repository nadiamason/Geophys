import numpy as np

infile = open("usgseditedeqs.csv", "r")
newfile = open("usgsgmthistearthquakes.txt", "w")
newfile.write("Year + date, update date, Latitude, Longitude, Depth, Ml, Mw, M0\n")

counter = 0
for line in infile:
    line = (line.strip()).split(",")
    if counter == 0:
        headers = line
        counter += 1
        continue
    
    # extracting data from file

    latitude = line[4]

    try:
        latitude = float(latitude) 
    except ValueError:
        line.pop(4)
        latitude = float(line[4]) 
    
    # getting year and date
    try:
        year = float(line[2])
        date = line[3]

    except ValueError:
        year = line[2][:4]
        try: 
            year = float(year)
            date = line[2][5:10]
        except ValueError:
            year = line[3][:4]
            date = line[3][5:10]
        

    longitude = str(float(line[5]))
    try:
        depth = float(line[6])
    except ValueError:
        depth = line[6]
        if depth == 'S':
            depth = 12
        elif depth == 'LC':
            depth = 33
    try:
        ml = float(line[7])
    except:
       ml = "None" 

    # if mw not given
    if line[8] == 'None':
        # shallow earthquakes
        if depth <= 33:
            mw = (ml - 0.73)/0.88
        # deep earthquakes
        else: 
            mw = (ml - 0.05)/1.09
    
    # if mw already given
    else:
        mw = float(line[8])

    m0 = 10**((1.5 * mw) + 9.1)

    newline = [year, date, latitude, longitude, depth, ml, round(mw, 2) , m0]
    newline = [str(x) for x in newline]
    for element in newline:
        newfile.write(element)
        newfile.write("  ")
    newfile.write("\n")

    
#Historical Tsunami Earthquakes from the NCEI Database
#Year  Mo  Da  Lat+N  Long+E  Dep  Mag
#1987  01  04  49.77  149.29  489  4.1
#1987  01  09  39.90  141.68  067  6.8