#!/usr/bin/python3
# Rex Tsai <chihchun@kalug.linux.org.tw>

import OsmApi
import csv
import sys
from pprint import pprint
from subprocess import call


def main():
    
    stones = {}
    with open('stone.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            stones[row[0]] = row[3]
            if(len(row[1])>0):
                stones[row[1]] = row[3]

    with open('100mountain.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            if(row[2] in stones):
                print ("%s %s" % (row[2], stones[row[2]]))
            else:
                print ("%s missing" % (row[2]))

if __name__ == '__main__':
    main()
