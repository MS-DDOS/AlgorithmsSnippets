from collections import OrderedDict
eventList = "ABETAVEQMMBUVHUJTJHQ"
startedBefore = -1
finishedBefore = 0
visited = []
degree = OrderedDict()
incrementNext = False
for i in range(len(eventList)): #O(n)
	if incrementNext:
		finishedBefore += 1
		degree[eventList[i-1]][1] = startedBefore
		incrementNext = False
	if eventList[i] in visited: #O(1)
		incrementNext = True
	else:
		startedBefore += 1
		degree[eventList[i]] = [finishedBefore,-1] #-1 is a sentinel value
	visited.append(eventList[i])
degree[eventList[len(eventList)-1]][1] = finishedBefore
for key, value in degree.items(): #O(n/2)
	print key, value[1]-value[0]

