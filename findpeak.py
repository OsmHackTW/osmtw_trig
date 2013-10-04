#!/usr/bin/python3
# Rex Tsai <chihchun@kalug.linux.org.tw>

import OsmApi
import csv
import sys
from pprint import pprint
from subprocess import call

stones = sys.argv[1:]

delta = 0.002
readonly = True
debug = True
show_nonexist = False

def searchosm(osm, lon, lat, delta):
    return osm.Map(lon-delta, lat-delta, lon+delta, lat+delta)

def matchnodes(nodes, tagname, tagvalue=None):
    for data in nodes:
        node = data['data']
        if(node['tag'] and tagname in node['tag']):
            if(tagvalue is None):
                yield node
            else:
                if (tagvalue == node['tag'][tagname]):
                    yield node
    pass

def ispeak(name):
    peaklist = ["山", "岳", "尖", "峰", "嶺"]
    for i in peaklist:
        if(name.endswith(i)):
            return True
    return False

def osmlink(node):
    links = ("http://www.openstreetmap.org/#map=13/%s/%s&layers=CN" % (node['lat'], node['lon']))
    if('id' in node):
        links += "\n" + "http://www.openstreetmap.org/browse/node/%s" % (node['id'])
    return links

def main():
    with open('stone.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
        # 點位名稱,,高度,種類,等,編號,材質,TWD97緯度,TWD97經度,TW67橫座標,TW67縱座標,所在地,狀況,備註,
        for row in spamreader:
            # ignore data without lat, lon
            if(len(row[7]) == 0 or len(row[8]) == 0):
                continue

            # refine the format
            row[5] = row[5].replace("◎本點","")
            row[5] = row[5].replace("●","")
            lat = row[7] = float(row[7]) # lat
            lon = row[8] = float(row[8]) # lon
            ele = row[2] = row[2].replace(",","")
    
            if((len(stones) == 0 or row[3] in stones) and (ispeak(row[0] or ispeak(row[1])))):
                print(row[0])

if __name__ == '__main__':
    main()
