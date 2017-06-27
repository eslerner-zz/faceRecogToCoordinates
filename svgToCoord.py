import numpy
import svg.path
import xml.dom
import svgpathtools
import math
from xml.dom import minidom
from svg.path import parse_path

svg_dom = minidom.parse("C:\Users\Emily\Downloads\Apple\homer-simpson.svg")
path_strings = [path.getAttribute('d') for path in svg_dom.getElementsByTagName('path')]
z = 0

for path_string in path_strings:
    path_data = parse_path(path_string)
    w, h = int(math.floor(path_data.length())), 2;

    LinePos = [[0 for x in range(w)] for y in range(h)]
    row = 0
    columns = 0
    for point in path_data:
        for point2 in range(0,1,int(1/.01)):
            x =  int(path_data.point(point2).real)
            y = int(path_data.point(point2).imag)
            print(x)
            print(y)

#grab the svg file
#xmlFile = minidom.parse("C:\Users\Emily\Downloads\Apple\homer-simpson.svg")

#path_strings = [path.getAttribute('d') for path in xmlFile.getElementsByTagName('path')]
#for path_string in path_strings:#for every string,
 #   path_data = parse_path(path_string) #return the data for that string (ex: start, controls, end) for eaach piece of info
  #  print(path_data)
   # for point in range(0,1):
    #    print(path_data.)





  #  length = path_data.length()
 #   for i in range(1,int(math.floor(length - 1))):
        #point = path_data.point(i)
       # print(point)
    #x = pointAtZero.x
    #print(length)
    #print(pointAtZero)



    #for i in range(path_data., int(math.floor(length))):
     #   path12 = path_data.point(i)
    #    print(path12)
    #print(length)
    #print(path_data)

#inside svg tags
#svgElems = xmlFile.getElementsByTagName("svg")[0]

#inside "g" tags
#gElems = svgElems.getElementsByTagName("g")[0]

#find the paths
#paths = gElems.getElementsByTagName("path")

#for every path line, get that instruction.
#for p in paths:
   # a = p.getAttribute('class')
 #   svgInstructions = p.getAttribute('d')
   # print(svgInstructions)