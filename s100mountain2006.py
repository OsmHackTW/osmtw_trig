#!/usr/bin/python3
# Rex Tsai <chihchun@kalug.linux.org.tw>

import OsmApi
import csv
import sys
import re
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

    with open('s100mountain2006.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            name = row[1]
            match = re.search("\[\[(.*?)(\|.*?)?\]\]", name)
            if(match.group(2)):
                name = match.group(2).replace("|","")
            else:
                name = match.group(1)
            if(name in stones):
                print ("%s %s" % (name, stones[name]))
            else:
                print ("%s missing" % (name))

if __name__ == '__main__':
    main()
