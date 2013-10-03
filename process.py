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
"一等三角點基線點",
"一等三角點基線點",
"一等三角點本點",
"一等三角點本點",
"一等三角點本點",
"一等三角點本點",
"一等三角點補點",
"二等三角點",
"三等三角點",
"四等三角點",
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
#"森林三角點",
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

osm = OsmApi.OsmApi(passwordfile="passwd", appid = 'RexBot', debug=debug, changesetauto=False)

with open('stone.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # 點位名稱,,高度,種類,等,編號,材質,TWD97緯度,TWD97經度,TW67橫座標,TW67縱座標,所在地,狀況,備註,
    for row in spamreader:
        if(row[3] in stones and not len(row[12])):
#            if("山" in row[0] or "岳" in row[0] or "尖" in row[0] or "峰" in row[0] or "嶺" in row[0]):
#                print ("%s" % (row[0]))

            lat = float(row[7])
            lon = float(row[8])
            data = osm.Map(lon-delta, lat-delta, lon+delta, lat+delta)
            match = []
            for i in data:
                if (i['data']['tag'] and (
                    ('natural' in i['data']['tag'] and "peak" in i['data']['tag']['natural']) or 
                    ('man_made' in i['data']['tag'] and 'survey_point' == i['data']['tag']['man_made'])
                    )):
                   match.append(i)

            if(len(match) == 1):
                   node = match[0]['data']
                   if 'ele' not in node['tag']:
                       node['tag']['ele'] = 0
                   if 'name' not in node['tag']:
                       node['tag']['name'] = ''
                   print ("%s %s %s %s" % (row[0], row[2], lat, lon))
                   print ("%s %s %s %s" % (node['tag']['name'], node['tag']['ele'], node['lat'], node['lon']))
            else:
                   print ("%d matched %s %s %s %s" % (len(match), row[0], row[2], lat, lon))

#            if(len(match) == 0):
#                print (data)
