#!/usr/bin/python3
# Rex Tsai <chihchun@kalug.linux.org.tw>

import OsmApi
import csv
import sys
from pprint import pprint
from subprocess import call

def main(argv=sys.argv):
    if(not argv[1:]):
        print ("%s: pointtype." % argv[0])
        return
    
    with open('stone.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
        # 點位名稱,,高度,種類,等,編號,材質,TWD97緯度,TWD97經度,TW67橫座標,TW67縱座標,所在地,狀況,備註,
        for row in spamreader:
            if(row[3] == argv[1]):
                if(len(row[12]) > 0 and row[12] != "找不到"):
                    pprint(row)

if __name__ == '__main__':
    main()
