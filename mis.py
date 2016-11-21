#maximal independent set

from scipy.stats import uniform
from math import sqrt, pi, ceil
from operator import itemgetter
import numpy as np
import pygraphviz as pgv
from collections import OrderedDict
import sys

def htmlcolor(r, g, b):
    def _chkarg(a):
        if isinstance(a, int): # clamp to range 0--255
            if a < 0:
                a = 0
            elif a > 255:
                a = 255
        elif isinstance(a, float): # clamp to range 0.0--1.0 and convert to integer 0--255
            if a < 0.0:
                a = 0
            elif a > 1.0:
                a = 255
            else:
                a = int(round(a*255))
        else:
            raise ValueError('Arguments must be integers or floats.')
        return a
    r = _chkarg(r)
    g = _chkarg(g)
    b = _chkarg(b)
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

'''
n*pi*r^2 = expected degree of a typical vertex
root(d/(n*pi)) = r
'''
def solveForR(n,degree):
	return sqrt((degree+1)/(n*pi))

def misUpperBound(n, degree):
	r = sqrt((degree+1)/(n*pi))
	triangle = 1/(((r**2)*sqrt(3))/4)
	density = pi/sqrt(12)
	return density/(((r/2)**2)*pi),triangle/2

def generatePoints(n):
	x = uniform.rvs(size=n)
	y = uniform.rvs(size=n)
	return zip(x,y)

def isCorrect(temp,sortedList):
	for i in temp:
		if i not in sortedList:
			return False
	return True

def slicePoints(pointList,r,currentTuple,currentTupleIndex,avgDegree):
	lowerIndex = 0
	upperIndex = 0
	indexCounter = currentTupleIndex - (avgDegree/2)
	
	if indexCounter >= 0:
		while True:
			if pointList[indexCounter][0] < (currentTuple[0]-r):
				lowerIndex = indexCounter
				break
			if indexCounter > 0:
				indexCounter -= 1
			else:
				lowerIndex = indexCounter
				break
	else:
		lowerIndex = 0

	indexCounter = currentTupleIndex + (avgDegree/2)
	if indexCounter <= len(pointList)-1:
		while True:
			#print "COMPARING:",pointList[indexCounter][0],"(",indexCounter,") AND",(currentTuple[0]+r),"(",currentTupleIndex,")",(pointList[indexCounter][0] > (currentTuple[0]+r))
			if pointList[indexCounter][0] > (currentTuple[0]+r):
				upperIndex = indexCounter
				break
			if indexCounter < len(pointList)-1:
				indexCounter += 1
			else:
				upperIndex = indexCounter
				break
	else:
		upperIndex = len(pointList)-1

	return (lowerIndex,upperIndex)

def distance(point1, point2):
	return sqrt(((point2[1]-point1[1])**2) + ((point2[0]-point1[0])**2))

def isEdge(point1, point2, r):
	return distance(point1,point2) <= r

def makeAdjacencyRow(sortedPoints, currentTuple, currentTupleIndex, r, avgDegree):
	windowIndices = slicePoints(sortedPoints,r,currentTuple,currentTupleIndex,avgDegree)
	indexCounter = windowIndices[1]
	edges = []
	while (indexCounter >= windowIndices[0]) and (indexCounter >= 0):
		if indexCounter != currentTupleIndex:
			if isEdge(currentTuple,sortedPoints[indexCounter],r):
				edges.append(indexCounter)
		indexCounter -= 1
	return edges	


def makeRGG(n,r,avgDegree):
	sortedPoints = sorted(generatePoints(n),key=itemgetter(0))
	G = {}
	indexCounter = 0
	for point in sortedPoints:
		#print point
		G[indexCounter] = makeAdjacencyRow(sortedPoints,point,indexCounter,r,avgDegree)
		#print indexCounter
		indexCounter += 1
	return (G,sortedPoints)

def outputToCSV(adjList,points):
	with open("graph.csv","w") as fout:
		fout.write("node,x,y\n")
		indexCounter = 0
		for point in points:
			fout.write(str(indexCounter)+","+str(point[0])+","+str(point[1])+"\n")
			indexCounter += 1

	maxLength = 0
	for i in range(len(adjList)):
		if len(adjList[i]) > maxLength:
			maxLength = len(adjList[i])

	with open("adjList.csv","w") as fout:
		fout.write("node")
		for i in range(maxLength):
			fout.write(",edge"+str(i))
		fout.write("\n")
		for record in range(len(adjList)):
			fout.write(str(record))
			for edge in adjList[record]:
				fout.write(","+str(edge))
			fout.write("\n")

	with open("adjListCompressed.csv","w") as fout:
		fout.write("node")
		for i in range(maxLength):
			fout.write(",edge"+str(i))
		fout.write("\n")
		for record in range(len(adjList)):
			fout.write(str(record))
			for edge in adjList[record]:
				if edge > record:
					fout.write(","+str(edge))
			fout.write("\n")

def makeRGGViz(adjList,points):
	r=255
	g=255
	b=255
	outputGraph = pgv.AGraph()
	colorShiftCounter = 0
	for key in adjList:
		outputGraph.add_node(key,style="filled",color="#2B2B2B",fillcolor=htmlcolor(r,g-colorShiftCounter,b-colorShiftCounter),pos=str(points[key][0])+","+str(points[key][1]),shape="circle")
		colorShiftCounter += 2
	colorShiftCounter = 0
	r = 200
	g = 0
	b = 0
	for key in adjList:
		for edge in adjList[key]:
			outputGraph.add_edge(key,edge,color=htmlcolor(r,g+colorShiftCounter,b+colorShiftCounter+1))
		colorShiftCounter+=2
	for i in range(len(points)):
		outputGraph.get_node(i).attr['pos']='{},{}!'.format(points[i][0]*20,points[i][1]*20)
	outputGraph.layout()
	outputGraph.draw("outputGraph.png")

def makeRGGVizWithMIS(adjList,points,mis):
	r=255
	g=255
	b=255
	outputGraph = pgv.AGraph()
	colorShiftCounter = 0
	for key in adjList:
		if key in mis:
			outputGraph.add_node(key,style="filled",color="#2B2B2B",fillcolor=htmlcolor(0,255,0),pos=str(points[key][0])+","+str(points[key][1]),shape="circle")
		else:
			outputGraph.add_node(key,style="filled",color="#2B2B2B",fillcolor=htmlcolor(247,89,89),pos=str(points[key][0])+","+str(points[key][1]),shape="circle")
		colorShiftCounter += 2
	colorShiftCounter = 0
	r = 200
	g = 0
	b = 0
	for key in adjList:
		for edge in adjList[key]:
			outputGraph.add_edge(key,edge,color="#2B2B2B")
	for i in range(len(points)):
		outputGraph.get_node(i).attr['pos']='{},{}!'.format(points[i][0]*20,points[i][1]*20)
	outputGraph.layout()
	outputGraph.draw("outputGraphWithMIS.png")

def makeRGGMISViz(indSet,points):
	outputGraph = pgv.AGraph()
	for key in indSet:
		outputGraph.add_node(key,style="filled",color="#2B2B2B",fillcolor=htmlcolor(0,255,0),pos=str(points[key][0])+","+str(points[key][1]),shape="circle")
		outputGraph.get_node(int(key)).attr['pos']='{},{}!'.format(points[int(key)][0]*20,points[int(key)][1]*20)
	outputGraph.layout()
	outputGraph.draw("outputGraphMIS.png")

def findMSI(adjList,indepset):
	if len(adjList) == 0:
		return indepset
	chosenVertex = adjList.popitem(last=False)
	for vertex in chosenVertex[1]:
		if vertex in adjList:
			for grandchild in adjList[vertex]:
				if grandchild in adjList:
					adjList[grandchild].remove(vertex)
			del adjList[vertex]
	indepset.append(chosenVertex[0])
	return findMSI(adjList,indepset)

def orderByDegree(adjList):
	return OrderedDict(sorted(adjList.items(), key=lambda (k,v):len(v)))

def maxIndependentSet(adjList):
	independentSet = []
	return findMSI(orderByDegree(adjList),independentSet)

n = int(sys.argv[1])
avgDegree = int(sys.argv[2])

circleUpperBound, triangleUpperBound = misUpperBound(n,avgDegree)
print "Circle Upper bound is:",circleUpperBound
print "Triangle Upper Bound is:",triangleUpperBound

'''
independentSetSizes = []
for trials in range(10):
	myGraph = makeRGG(n,solveForR(n,avgDegree),avgDegree)
	independentSetSizes.append(len(maxIndependentSet(myGraph[0])))
print 
'''

myGraph = makeRGG(n,solveForR(n,avgDegree),avgDegree)
mis = maxIndependentSet(myGraph[0])
print "Actual size is:",len(mis)
makeRGGViz(myGraph[0],myGraph[1])
makeRGGVizWithMIS(myGraph[0],myGraph[1],mis)
makeRGGMISViz(mis,myGraph[1])
outputToCSV(myGraph[0],myGraph[1])



