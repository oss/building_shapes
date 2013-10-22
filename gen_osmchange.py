import urllib2
import xml.etree.ElementTree as ET
from pprint import pprint

class Way():
    def __init__(self, way, nodes):
        self.nodes = []
        self.tags = {}
        self.avg_point = [0, 0]
        for nd in way.findall('nd'):
            node = nodes[nd.attrib['ref']]
            self.nodes.append(node)
            self.avg_point[0] += float(node.attrib['lon'])
            self.avg_point[1] += float(node.attrib['lat'])
        self.avg_point[0] /= len(self.nodes)
        self.avg_point[1] /= len(self.nodes)
        for tag in way.findall('tag'):
            self.tags[tag.attrib['k']] = tag.attrib['v']

debug = False

base_apiurl = 'http://api.openstreetmap.org' if debug == False else 'http://api06.dev.openstreetmap.org'
boundb_apiurl = base_apiurl + '/api/0.6/map?bbox={0},{1},{2},{3}'

bush_livi = [-74.4736, 40.5096, -74.4332, 40.5283]
college_ave = [-74.4576, 40.4905, -74.4372, 40.5068]
cook_douglass = [-74.4453, 40.4777, -74.4276, 40.4887]

locations = [bush_livi, college_ave, cook_douglass]

responses = [urllib2.urlopen(boundb_apiurl.format(*location)) for location in locations]
roots = [ET.fromstring(response.read()) for response in responses]

osm_ways = []

for root in roots:
    nodes = {}
    for node in root.findall('node'):
        nodes[node.attrib['id']] = node

    for way in root.findall('way'):
        building = False
        for tag in way.findall('tag'):
            if tag.attrib['k'] == "building" and tag.attrib['v'] == "yes":
                building = True
        if building:
            osm_ways.append(Way(way, nodes))

for way in osm_ways:
    pprint(way.nodes)
    pprint(way.tags)
    pprint(way.avg_point)
