import hashlib, csv

def getHash(st):
    m = hashlib.md5()
    m.update(st)
    return m.hexdigest()
                    

def generetBusStops(filename):
    '''
    reads the csv file passed and returns the buses along with their corresponding mybmtc url 
    in form of a hash
    '''
    f = open(filename);
    csv_f = csv.reader(f)
    busStops = {}
    
    i = 0;
    for row in csv_f:
        if i!=0:
            busStops[getHash(row[0])] = row
        i+=1
    #getRoutes(route_url)
    return busStops
    
print generetBusStops("busstops.txt")