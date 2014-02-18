
#!/usr/bin/env python
import sys
import sys, traceback
import sqlite3 as lite
import requests
import json
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

def loadBusstopMapJSON():
    con = lite.connect('bmtc.sqlite')
    cur = con.cursor()
    cur.execute("select map_link, route_no  FROM routes where map_json_content is null")
    rows = cur.fetchall()
    cur2 = con.cursor()
    for row in rows:
        try:
            url = row[0]
            route_no = row[1]
            print url
            html_src = requests.get(url)
            soup = BeautifulSoup(html_src.content)
            scripts = soup.findAll("script")
            our_script = scripts[6]
            script_text = our_script.text
            script_text = script_text.replace("jQuery.extend(Drupal.settings, ","")
            script_text = script_text[:-2]
            #print script_text
            data = json.loads(script_text)
            print data['busstops']
            document ={"map_json_content": json.dumps(data['busstops']), "route_no":route_no}
            cur2.execute("update routes set map_json_content=:map_json_content where route_no=:route_no", document)
            con.commit()
        except:
            pass
    con.close()

def loadBusStop():
    con = lite.connect('bmtc.sqlite')
    cur = con.cursor()
    cur.execute("select map_json_content, route_no  FROM routes where map_json_content is not null")
    rows = cur.fetchall()
    cur2 = con.cursor()
    for row in rows:
        try:
            map_json_content = row[0]
            route_no = row[1]
            #print map_json_content
            order = 0
            data = json.loads(map_json_content)
            for stop in data:   
                #print stop             
                order = order+1
                print order
                print route_no
                #document ={"name": stop['busstop'], "lat": stop['latlons'][0], "lng": stop['latlons'][1]}
                #cur2.execute('INSERT INTO busstop (name,lat,lng) VALUES (:name, :lat, :lng)', document)

                document_2 ={"busstop": stop['busstop'], "route_no": route_no, "serial": str(order)}
                cur2.execute('INSERT INTO bus_route (route_no,busstop,serial) VALUES (:route_no, :busstop, :serial)', document_2)
                print "Done"
                con.commit()

        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60

    con.close()

#loadBusstopMapJSON()
#loadRoutes(start_page_number,final_page_number) 
loadBusStop()
