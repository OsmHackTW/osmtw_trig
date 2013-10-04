#!/usr/bin/python3
# Rex Tsai <chihchun@kalug.linux.org.tw>

import OsmApi
import csv
import sys
from pprint import pprint
from subprocess import call


def main():
    
    stones = []
    with open('stone.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            stones.append(row[0])
            if(len(row[1])>0):
                stones.append(row[1])

    with open('100mountain.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if(row[2] not in stones):
                print ("%s" % (row[2]))

if __name__ == '__main__':
    main()
