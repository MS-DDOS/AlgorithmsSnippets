import sys

def V(num_cards):
	v = [0,1]				#Array used for V(n) estimations
	take_points = [0,1]		#Array used for take point estimations
	take_point = 0

	# Calculate values for V(n) up to num_cards
	for n in range(2, num_cards + 1):
		expected_value = 0
	
		# For the current n, get the expected value for all cards
		for i in range(1, n + 1):
			take_value = 1 + v[n - i]
			ignore_value = v[n - 1]

			expected_value += max(take_value, ignore_value)

			
			if take_value > ignore_value:
				take_point = i
		
		# Divide the summed expected values by n
		expected_value /= float(n)

		# Add estimated values to their respective arrays
		v.append(expected_value)
		take_points.append(take_point)

	print take_points

	for i in range(1, 4):
		print "k: %d" % i
		print "n: %d" % (2**i)
		print "V(n): %f" % v[2**i]
		print "Take Point: %d\n" % take_points[2**i]


def main():
	if len(sys.argv) < 2:
		print "Requires value for n"
	elif len(sys.argv) > 2:
		print "Too many arguments"
	else:
		V(int(sys.argv[1]))

main()