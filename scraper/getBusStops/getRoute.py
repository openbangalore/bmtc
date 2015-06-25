'''
Source of data: MyBMTCS and https://github.com/openbangalore/bmtc

how it works? 

Picks the buses from busroutes.csv 
Gets their route from mybmtc in form of json

Start from while loop to understand the flow complete

1) Searches if the bus is present in the local files
2) If the bus is not found locally then looks up online 

To do:
Need to append the url of the bus found online locally 
'''
import signal, sys
import requests, json, csv
from BeautifulSoup import BeautifulSoup


def getRoutes(url):
    soup = BeautifulSoup(requests.get(url).text)
    scripts = soup.findAll('script')
    extracted = scripts[6].text.split('busstops":')[1].split(',"getdirections"')[0]
    js = json.loads(extracted)
    print json.dumps(js, sort_keys=True, indent=4) #printing json here 


def generateBusData(filename):
    '''
    reads the csv file passed and returns the buses along with their corresponding mybmtc url 
    in form of a hash
    '''
    f = open(filename);
    csv_f = csv.reader(f)
    buses = {}
    
    for row in csv_f:
        #print row
        bus_no = row[0].lower()
        distance = row[1]
        starting = row[2]
        ending = row[3]
        route_url = row[4]
        buses[bus_no] = route_url
        #getRoutes(route_url)
    return buses

def getNewBus(busno):
	'''
	Given any bus Number, this prints its route in one direction 
	You can print routes in both directions by doing a small mod 
	'''
	bus_url = "http://www.mybmtc.com/route/search/"+busno+"/0"
	soup = BeautifulSoup(requests.get(bus_url).text)
	m = soup.find('a', {'id':'mapview'})
	#use findAll for both directions and then loop to print
	try: 
		getRoutes(m['href'])
	except:
		print "Bus not found online also, sorry"
	

buses = generateBusData('busroutes.txt')



while 1:
    #Given a bus number this returns the json file containing bus route
    try:
    	userInput = raw_input("Enter Bus No Here: ").lower()
        getRoutes(buses[userInput])
        print "\n\n"
    except KeyboardInterrupt:
		print "Exiting"
		sys.exit()
    except :
    	print "Searching Online for Bus records"
		getNewBus(userInput)
		
'''
You can make this call for all the buses in busroutes.csv file and save it a DB 
'''
