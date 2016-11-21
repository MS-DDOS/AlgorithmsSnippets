from collections import OrderedDict
from Queue import PriorityQueue as pq
colorCounter = 0
colors = OrderedDict()
eventColors = OrderedDict()
eventList = "ABETAVEQMMBUVHUJTJHQ"

for i in range(len(eventList)):
	if eventList[i] in eventColors.keys():
		colors[eventColors[eventList[i]]] = True
	else:
		didSet = False
		for key, value in colors.items():
			if value == True:
				colors[key] = False
				eventColors[eventList[i]] = key
				didSet = True
				break
		if didSet != True:
			colors[colorCounter] = False
			eventColors[eventList[i]] = colorCounter
			colorCounter += 1

visited = []
for i in range(len(eventList)):
	if eventList[i] in visited:
		continue
	print eventList[i],eventColors[eventList[i]]
	visited.append(eventList[i])