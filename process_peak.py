#!/usr/bin/python3
# Rex Tsai <chihchun@kalug.linux.org.tw>

import OsmApi
import csv
import sys
from pprint import pprint
from subprocess import call


comment = u"三角點 基石資料"
readonly = False
delta = 0.002
debug = True
stones = []

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
    osm = OsmApi.OsmApi(passwordfile="passwd", appid = 'RexBot', debug=debug, changesetauto=False)
    
    if (readonly is not True):
        print ("changeset id %d" % (osm.ChangesetCreate({u"comment": comment})), file=sys.stderr)
    
    with open('stone.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
        # 點位名稱,,高度,種類,等,編號,材質,TWD97緯度,TWD97經度,TW67橫座標,TW67縱座標,所在地,狀況,備註,
        for row in spamreader:
            # ignore data without lat, lon
            if(len(row[7]) == 0 or len(row[8]) == 0):
                continue
            # ignore if the stone is missing.
            if(len(row[12]) > 0):
                continue
            if (not ispeak(row[0]) and not ispeak(row[1])):
                continue
            # refine the format
     
            row[5] = row[5].replace("◎本點","")
            row[5] = row[5].replace("●","")
            lat = row[7] = float(row[7]) # lat
            lon = row[8] = float(row[8]) # lon
            ele = row[2] = row[2].replace(",","")
    
            if(len(stones) == 0 or row[3] in stones):
                data = searchosm(osm, lon, lat, 0.002)
    
                match = list(matchnodes(data, "natural", "peak"))

                # found more then one peaks near by. ignore it for now.
                if(len(match) > 1):
                    for node in (match):
                        pprint(node)
                        print(osmlink(node))
    
                # node not exist.
                if(len(match) == 0):
                    node = { 
                            'lat': lat,
                            'lon': lon,
                            'tag': {
                                'name': row[0],
                                'name:zh': row[0],
                                'natural': 'peak',
                                'ele': ele,
                                }
                            }
                    if(len(row[1])>0):
                        node['tag']['alt_name'] = row[1]

                    if (not readonly):
                        osm.NodeCreate(node)
    
                # node exist, only update names.
                if(len(match) == 1):
                    node = match[0]
                    if('name' in node['tag'] and (row[0] in node['tag']['name'] or row[1] in node['tag']['name'])):
                        node['tag']['name'] = row[0]
                        node['tag']['name:zh'] = row[0]
                        if(len(row[1])>0):
                            node['tag']['alt_name'] = row[1]
                        # update ele, only when not set.
                        if('ele' not in node['tag']):
                            node['tag']['ele'] = row[2]
                        if (not readonly):
                            osm.NodeUpdate(node)
                    else:
                        # found different peak.
                        pprint(node)
                        print(osmlink(node))

    if (not readonly):
        osm.ChangesetClose()

if __name__ == '__main__':
    stones = sys.argv[1:]
    main()
