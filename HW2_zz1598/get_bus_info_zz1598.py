'''
PUI2016
HW2_zz1598
Assignment 2

Prompt for: xxxx-xxxx-xxxx-xxxx-xxxx <BUS_LINE> <BUS_LINE>.csv
Read: Lon, Lat in <['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']>
-----
the segment storing the stop_name and stop_status info in json has the following structure:
"StopPointName": "GATES AV/CENTRAL AV",
"Extensions": {
    "Distances": {
        "CallDistanceAlongRoute": 7373.74,
        "StopsFromCall": 0,
        "PresentableDistance": "at stop"
'''

# url format:  http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=YOUR_KEY&VehicleMonitoringDetailLevel=calls&LineRef=B52
# Key:  36659132-f439-4afa-b9be-4b034368fd2b

import json
import urllib
import codecs

mta_serviceurl =  "http://bustime.mta.info/api/siri/vehicle-monitoring.json?"

while True:
    key_bus_f = raw_input("Enter API Key, Bus Line, filename: ").split()
    key = key_bus_f[0]
    busline = key_bus_f[1]
    fname = key_bus_f[2]
    if len(key) < 1 or len(busline) < 1 or fname < 1:
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

    # fhand = codecs.open('bus_json.js', 'w+', "utf-8")   write in a json file to inspect the format and content
    # fhand.writelines(json.dumps(data_js, indent=4))
    # fh_js = open('bus_json.js', 'r')  open the saved json file to retrieve information without API call, for testing
    # data = fh_js.read()
    # data_js = json.loads(str(data))


    fh_bus = open(fname, 'w+')  #create a csv file to write retrieved info
    fh_bus.writelines('Latitude,Longitude,Stop Name,Stop Status\n')

    lst_bus_activity = data_js['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

    for dic in lst_bus_activity:
        lat = dic['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
        lon = dic['MonitoredVehicleJourney']['VehicleLocation']['Longitude']

        if len(dic['MonitoredVehicleJourney']["OnwardCalls"]) < 1:
            stop_name, stop_status = 'N/A', 'N/A'
        else:
            stop_name = dic['MonitoredVehicleJourney']["OnwardCalls"]["OnwardCall"][0]["StopPointName"]
            stop_status = dic ['MonitoredVehicleJourney']["OnwardCalls"]["OnwardCall"][0]["Extensions"]["Distances"]["PresentableDistance"]
        print '{},{},{},{}'.format(lat, lon, stop_name, stop_status)
        fh_bus.writelines('{},{},{},{}\n'.format(lat, lon, stop_name, stop_status))

    break

