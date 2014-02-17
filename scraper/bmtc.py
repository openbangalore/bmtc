
#!/usr/bin/env python
import sys
import sqlite3 as lite
import requests
from BeautifulSoup import BeautifulSoup
final_page_number = 111
start_page_number = 1
try:
    start_page_number = int(sys.argv[1])
except:
    print "Running from page 1"


url ="http://www.mybmtc.com/service/timings/gns/General%20Services"

def loadRoutes(start_page_number,final_page_number):
    con = lite.connect('bmtc.sqlite')
    cur = con.cursor()
    for page_number in range(start_page_number,final_page_number):
        print "========================="+str(page_number)+"=========================================="
        html_url = ""
        if page_number == 1:
            html_url = "http://www.mybmtc.com/service/timings/gns/General%20Services"
        else:
            html_url = "http://www.mybmtc.com/service/timings/gns/General%20Services?page="+str(page_number)
        
        html_src = requests.get(html_url)

        soup = BeautifulSoup(html_src.content)
        tables = soup.findAll("table")
        listing_table = tables[0]
        #print listing_table
        first = True
        for i in listing_table.findAll('tr'):
            if first:
                row = i.text
                first = False
            else:
                route = i.find("p", { "id" : "routeno" })
                route_text = (route.text).replace("Route NO:","")

                origin = i.find("p", { "id" : "origin" })
                origin_text = (origin.text).replace("Origin :","")

                destination = i.find("p", { "id" : "destination" })
                destination_text = (destination.text).replace("Destination :","")

                viewbusstop = i.find("p", { "id" : "viewbusstop" })
                viewbusstop_anchor = viewbusstop.findAll("a")
                buststop_list = viewbusstop_anchor[0]['href']
                buststop_map = viewbusstop_anchor[1]['href']

                document = {"route_no":route_text,"origin":origin_text,"destination":destination_text, "map_link":buststop_map, "busstops_link":buststop_list}                
                cur.execute('INSERT INTO routes (route_no, origin, destination, map_link, busstops_link) VALUES (:route_no, :origin, :destination, :map_link, :busstops_link)', document)
                print document
                con.commit()
    con.close()

loadRoutes(start_page_number,final_page_number) 