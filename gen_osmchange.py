import urllib2
import xml.etree.ElementTree as ET
from pprint import pprint

debug = False

base_apiurl = 'http://api.openstreetmap.org' if debug == False else 'http://api06.dev.openstreetmap.org'
boundb_apiurl = base_apiurl + '/api/0.6/map?bbox={0},{1},{2},{3}'

bush_livi = [-74.4736, 40.5096, -74.4332, 40.5283]
college_ave = [-74.4576, 40.4905, -74.4372, 40.5068]
cook_douglass = [-74.4453, 40.4777, -74.4276, 40.4887]

response = urllib2.urlopen(boundb_apiurl.format(*bush_livi))
root = ET.fromstring(response.read())

nodes = {}

for node in root.findall('node'):
    nodes[node.attrib['id']] = node

pprint(nodes)
