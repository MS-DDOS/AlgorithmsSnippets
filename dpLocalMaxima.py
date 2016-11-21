from random import randint
from copy import deepcopy

#O(n^2) time
#O(n) space

def findLongestIncreasing(seq):
	lengths = []
	for element in seq:
		didFindSpot = False
		for i in range(len(lengths)):
			if element <= lengths[i]:
				lengths[i] = element
				didFindSpot = True
				break
		if didFindSpot != True:
			lengths.append(element)
	return lengths

def findLongestDecreasing(seq):
	lengths = []
	for element in seq:
		didFindSpot = False
		for i in range(len(lengths)):
			if element >= lengths[i]:
				lengths[i] = element
				didFindSpot = True
				break
		if didFindSpot != True:
			lengths.append(element)
	return lengths

def findLongestBitonic(seq):
	lis = [1 for x in range(len(seq))]
	lds = deepcopy(lis)

	for i in range(1,len(seq)):
		for j in range(i):
			if seq[i] > seq[j] and lis[i] < lis[j]+1:
				lis[i] = lis[j]+1

	for i in range(len(seq)-2)[::-1]:
		for j in range(len(seq)-1)[::-1]:
			if seq[i] > seq[j] and lds[i] < lds[j]+1:
				lds[i] = lds[j]+1

	maxVal = lis[0] + lds[0] - 1
	for i in range(len(seq)):
		if lis[i] + lds[i] - 1 > maxVal:
			maxVal = (lis[i] + lds[i]) - 1
	return maxVal

#mySeq = [30,58,74,44,22,45,74,68,60,67,24,73,36,13,42,46,55,69]
#mySeq = [30,58,74,44,22,45,74,68,60]
#mySeq = [randint(1,100) for x in range(100)]
mySeq = [54, 76, 30, 44, 74, 15, 78, 67, 36, 46, 11, 77, 42, 49, 82, 73, 80, 66, 52, 58, 22, 68, 35, 40, 24, 13, 55, 27, 39, 16, 43, 93, 61, 53, 94, 49, 74, 45, 60, 83, 18, 73, 42, 69, 67, 22, 61, 30, 63, 51, 62]
mySeq = mySeq[:5]
print findLongestIncreasing(mySeq)
print findLongestIncreasing(mySeq[::-1])

print "Sequence is:"
print mySeq
print findLongestBitonic(mySeq)
print findLongestBitonic(mySeq[::-1])
