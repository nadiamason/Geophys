infile = open("histearthquakes.csv", "r")
newfile = open("gmthistearthquakes.txt", "w")
newfile.write("Year, Date, Latitude, Longitude, Depth, Ml, Mw")

counter = 0
for line in infile:
    line = (line.strip()).split(",")
    if counter == 0:
        headers = line
        counter += 1
        continue
    
    # extracting data from file
    year = line[2]
    date = line[3]
    latitude = str(float(line[4]) * -1)
    longitude = str(float(line[5]))
    try:
        depth = float(line[6])
    except ValueError:
        depth = line[6]
        if depth == 'S':
            depth = 12
        elif depth == 'LC':
            depth = 33

    ml = float(line[7])

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
        mw = line[8]

    newline = [year, date, latitude, longitude, depth, ml, mw]
    newline = [str(x) for x in newline]
    for element in newline:
        newfile.write(element)
        newfile.write("  ")
    newfile.write("\n")

    
#Historical Tsunami Earthquakes from the NCEI Database
#Year  Mo  Da  Lat+N  Long+E  Dep  Mag
#1987  01  04  49.77  149.29  489  4.1
#1987  01  09  39.90  141.68  067  6.8