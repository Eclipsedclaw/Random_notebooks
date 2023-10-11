#!/usr/bin/env python
# coding: UTF-8

import sys
import pandas as pd

year = 2021
month = 3
day = 21
altitude = 30000 #m

g = 10.0

def main():
    infile = pd.read_csv("../../launchsite.csv")
    
    for i in range(len(infile)):
        name1 = infile['name1'][i].replace(" ", "_")
        name2 = infile['name2'][i].replace(" ", "_")
        latitude = infile['latitude'][i]
        longtitude = infile['longtitude'][i]
        comments = infile['comments'][i]
        outfilename = "{}_{}_{}_{}_{}_alt{}m.inp".format(name1, name2, year, month, day, altitude) 
        with open(outfilename, "w") as f:
            f.write("2 2\n")
            f.write("{} {} {} {} {} {} {}\n".format(year, month, day, latitude, longtitude, altitude, g) )

if __name__=="__main__":
    main()

