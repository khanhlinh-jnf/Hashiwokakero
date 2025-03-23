def init(data):
	data.insert(0, [0] * len(data[0]))
	data.append([0] * len(data[0]))

	for i in range(len(data)):
		data[i].insert(0, 0);
	
	for i in range(len(data)):
		data[i].append(0)  

	neighbors = {}
	for idx, rows in enumerate(data):
		for jdx, item in enumerate(rows):
			if item > 0: neighbors[(idx, jdx)] = []
	
	def findClosestNeighbor(pos):
		ax, ay = pos 
		closestNeighbor = []
		
		# right 
		if ay == len(data[0]) - 1: closestNeighbor.append(None) 
		for dy in range(1, len(data[0]) - ay):
			neighbor = (ax, ay + dy)
			if neighbor in neighbors:
				closestNeighbor.append(neighbor)
				break 
			else:
				if dy == len(data[0]) - 1 - ay: closestNeighbor.append(None) 

		# bottom 
		if ax == len(data) - 1: closestNeighbor.append(None)
		for dx in range(1, len(data) - ax):
			neighbor = (ax + dx, ay)
			if neighbor in neighbors:
				closestNeighbor.append(neighbor)
				break 
			else:	
				if dx == len(data) - 1 - ax: closestNeighbor.append(None) 

		# left 
		if (ay == 0): closestNeighbor.append(None)
		for dy in range(1, ay + 1):
			neighbor = (ax, ay - dy)
			if neighbor in neighbors:
				closestNeighbor.append(neighbor)
				break 
			else:
				if dy == ay: closestNeighbor.append(None) 

		# up 
		if (ax == 0): closestNeighbor.append(None)
		for dy in range(1, ax + 1):
			neighbor = (ax - dy, ay)
			if neighbor in neighbors:
				closestNeighbor.append(neighbor)
				break 
			else:
				if dy == ax: closestNeighbor.append(None)

		return closestNeighbor
	
	for pos in neighbors:
		closestNeighbors = findClosestNeighbor(pos) 
		neighbors[pos] = closestNeighbors

	return data, neighbors
