def readFile(fileName):
	arr = []
	number = fileName.split('-')[1]
	number = number.split('.')[0] 
	with open(fileName, 'r') as fin:
		for line in fin:
			line = line.strip() # remove space
			if not line: continue
			row = list(map(int, line.split(',')))
			arr.append(row)
	return arr, number

