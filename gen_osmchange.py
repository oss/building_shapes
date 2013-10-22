import urllib2
import xml.etree.ElementTree as ET
import sys
import Polygon, Polygon.IO
from pprint import pprint
from scipy import spatial

class Way():
    def __init__(self, way, nodes):
        self.nodes = []
        self.tags = {}
        self.avg_point = [0, 0]
        coords = []
        for nd in way.findall('nd'):
            node = nodes[nd.attrib['ref']]
            self.nodes.append(node)
            x = float(node.attrib['lon'])
            y = float(node.attrib['lat'])
            coords.append([x, y])
            self.avg_point[0] += x
            self.avg_point[1] += y
        self.polygon = Polygon.Polygon(coords)
        self.avg_point[0] /= len(self.nodes)
        self.avg_point[1] /= len(self.nodes)
        for tag in way.findall('tag'):
            self.tags[tag.attrib['k']] = tag.attrib['v']

def make_ways(root):
    nodes = {}
    ways = []
    for node in root.findall('node'):
        nodes[node.attrib['id']] = node

    for way in root.findall('way'):
        building = False
        for tag in way.findall('tag'):
            if tag.attrib['k'] == "building" and tag.attrib['v'] == "yes":
                building = True
        if building:
            ways.append(Way(way, nodes))

    return ways

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
    osm_ways.extend(make_ways(root))

osm_tree = spatial.KDTree([way.avg_point for way in osm_ways])

our_root = ET.parse(sys.argv[1])
our_ways = make_ways(our_root)

pairs = []
for way in our_ways:
    index = osm_tree.query([way.avg_point])[1][0]
    pairs.append([way, osm_ways[index]])

replace_pairs = []
for pair in pairs:
    intersect = pair[0].polygon & pair[1].polygon
    union = pair[0].polygon | pair[1].polygon
    jaccard = intersect.area() / union.area()
    if jaccard >= float(sys.argv[2]) / 100:
        replace_pairs.append(pair)
    else:
        replace_pairs.append([pair[0], None])

pprint(replace_pairs)
