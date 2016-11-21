def isShuffle(x,y,z):
	n = len(x)
	m = len(y)
	r = len(z)
	if r != n + m:
		return False
	S = [[False for i in range(m)] for j in range(n)]
	S[0][0] = True
	for i in range(1,n):
		S[i][0] = S[i-1][0] and (z[i-1] == x[i-1])
	for j in range(1,m):
		S[0][j] = S[0][j-1] and (z[j-1] == y[j-1])
	for i in range(1,n):
		for j in range(1,m):
			S[i][j] = ((z[i+j-1] == x[i-1]) and S[i-1][j]) or ((z[i+j-1] == y[j-1]) and S[i][j-1])
	for row in S:
		print row
	return S[n-1][m-1]

shuffle = "ABCDEFG"
s1 = "ABDG"
s2 = "CEF"
print isShuffle(s1,s2,shuffle)