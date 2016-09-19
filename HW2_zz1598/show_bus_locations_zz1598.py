'''
PUI2016
HW2_zz1598
Assignment 1

To Do:
Prompt for: <API key>, <Bus Line>
Read Json file and get : Lon, Lat in <['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']>
Print info
'''

#url format:  http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=YOUR_KEY&VehicleMonitoringDetailLevel=calls&LineRef=B52
#Key:  36659132-f439-4afa-b9be-4b034368fd2b


import json
import urllib
import codecs

mta_serviceurl =  "http://bustime.mta.info/api/siri/vehicle-monitoring.json?"

while True:
    key_busline = raw_input("Enter API Key & Bus Line: ").split()
    key = key_busline[0]
    busline = key_busline[1]
    if len(key) < 1 or len(busline) < 1:
        break

    url = mta_serviceurl + urllib.urlencode({'key':key,'VehicleMonitoringDetailLevel':'calls','LineRef':busline })
    print 'Retrieving', url

    data = urllib.urlopen(url).read()
    print 'Retrieved', len(data), 'characters'

    try:
        data_js = json.loads(str(data))

    except:
        data_js = None
        print '==Failure to Retrieve=='
        continue

    #fhand = codecs.open('bus_json.js', 'w', "utf-8")   write in a json file to inspect the format and content
    #fhand.writelines(json.dumps(data_js, indent=4))

    lst_bus_activity = data_js['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    bus_count = len(lst_bus_activity)
    print 'Bus Line: ', busline
    print 'Number of Active Buses: ',bus_count

    num = 0
    for dic in lst_bus_activity:
        lat = dic['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
        lon = dic['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
        print 'Bus {} is at latitude {} and longitude {}'.format(num, lat, lon)
        num += 1

    break






