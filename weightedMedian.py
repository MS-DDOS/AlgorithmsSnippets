from copy import deepcopy

def weightedMedian(elements,n):
    elements.sort() #use std library quicksort
    sumE = 0
    median = 0
    while sumE < 0.5:
        median += 1
        sumE += elements[median]
    return median

def select(elements,start,end,i):
	newElems = deepcopy(elements)
	newElems.sort()
	return newElems[i-1]

def linearWeightedMedian(elements,start,end,sumleft,sumright):
	i = (end - start)/2 #O(1)
	median = select(elements,start,end,i) #O(n)
	partitionElements(elements,start,end,median) #O(n)
	for j in range(start,i): #O(n/2)
		sumleft += elements[j] 
	for j in range(i,end): #O(n/2)
		sumright += elements[j]
	if sumleft < .5 and sumright <= .5:
		return elements[i]
	if sumleft >= .5:
		elements[i] += sumright
		return linearWeightedMedian(elements,start,i,0,sumright)
	return linearWeightedMedian(elements,i,end,sumleft,0)

X = [.1,.35,.05,.1,.15,.05,.2]
print linearWeightedMedian(X,0,len(X),0.0,0.0)