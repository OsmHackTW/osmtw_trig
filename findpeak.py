#!/usr/bin/python3
# Rex Tsai <chihchun@kalug.linux.org.tw>

import OsmApi
import csv
import sys
from pprint import pprint
from subprocess import call

delta = 0.002
readonly = True
debug = True

osm = OsmApi.OsmApi(passwordfile="passwd", appid = 'RexBot', debug=debug, changesetauto=False)

stones = [
"一等三角點基線點",
"一等三角點本點",
"一等三角點補點",
"二等三角點",
"三等三角點",
"四等三角點",
"森林三角點",
#"土地調查局測量原點",
#"土地調查局三等三角點",
#"內政部一等三角點補點",
#"內政部二等三角點補點",
#"內政部三等三角點補點",
#"聯勤二等三角點補點",
#"聯勤三等三角點補點",
#"陸軍三等三角點補點",
#"千岳俱樂部仿製二等三角點",
#"千岳俱樂部仿製三等三角點",
#"仿製三等三角點",
#"土地調查局圖根點",
#"圖根補點",
#"總督府圖根補點",
#"殖產局三角補點",
#"殖產局圖根三角補點",
#"殖產局圖根補點",
#"殖產局補點",
#"省政府圖根補點",
#"總督府三角點",
#"總督府點",
#"總督府柱",
#"內務局三角點" 
#"內務局補助三角點",
#"一等水準點",
#"北市三角點",
#"北市都市計畫點",
#"北市地測點",
#"北市地測精幹點",
#"北市",
#"北縣三角點",
#"北縣都市計畫點",
#"基隆",
]


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
            # ignore if the stone is missing.
            if(len(row[12]) > 0):
                continue
            # refine the format
     
            row[5] = row[5].replace("◎本點","")
            row[5] = row[5].replace("●","")
            lat = row[7] = float(row[7]) # lat
            lon = row[8] = float(row[8]) # lon
            ele = row[2] = float(row[2].replace(",",""))
    
            if(row[3] not in stones and (ispeak(row[0] or ispeak(row[1])))):
                print(row[3])

if __name__ == '__main__':
    main()
