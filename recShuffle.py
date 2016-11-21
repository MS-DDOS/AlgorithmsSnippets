def isShuffle(x,y,z):
	print "passing in:"
	print "\tx:",x
	print "\ty:",y
	print "\tz:",z
	if len(x) == 0:
		print "terminated because len(x) is 0"
		return y == z
	if len(y) == 0:
		print "terminated because len(y) is 0"
		return x == z

	#ic1 = (z[-1] == x[-1])
	#ic2 = isShuffle(x[:-1],y,z[:-1])
	#ic3 = (z[-1] == y[-1])
	#ic4 = isShuffle(x,y[:-1],z[:-1])
	return ((z[-1] == x[-1]) and isShuffle(x[:-1],y,z[:-1])) or ((z[-1] == y[-1]) and isShuffle(x,y[:-1],z[:-1]))
	#return (ic1 and ic2) or (ic3 and ic4)

shuffle = "ABCDEFG"
s1 = "ABDG"
s2 = "CEF"
print isShuffle(s1,s2,shuffle)