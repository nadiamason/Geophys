# opening focal mechanism data
from shapely.geometry import polygon


infile = open("m0beachballsnz.txt")

newfile = open("convertedlong.txt", "w")

for line in infile:
    words = line.split()
    try: 
        long = float(words[0])

    except:
        continue
    
    if long < 0:
        difference = 180 - abs(long)
        new_long = 180 + difference
        words[0] = new_long

    words = [str(x) for x in words]

    line = ' '.join(words)
        
    newfile.write(line)
    newfile.write("\n")
        