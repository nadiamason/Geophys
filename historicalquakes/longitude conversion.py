# opening focal mechanism data
from shapely.geometry import polygon


infile = open("usgsgmthistearthquakes.txt")

newfile = open("convertedusgsgmteqs.txt", "w")

for line in infile:
    words = line.split()
    try: 
        long = float(words[3])

    except:
        continue
    
    if long < 0:
        difference = 180 - abs(long)
        new_long = 180 + difference
        words[3] = new_long

    words = [str(x) for x in words]

    line = ' '.join(words)
        
    newfile.write(line)
    newfile.write("\n")
        