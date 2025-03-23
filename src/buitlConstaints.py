from pysat.formula import CNF
from src.satBridgeSum import bridge_sum_CNF_opt as bridge_sum
# from src.satBridgeSum import generate_CNF_quick
import math
import os  

def buildConstraints(field, number):
	class Node:
		def __init__(
				self,
				weight,
			    horizontal_bridge1 = None,
				horizontal_bridge2 = None,
				vertical_bridge1 = None,
				vertical_bridge2 = None):
			self.weight = weight
			self.h1 = horizontal_bridge1
			self.h2 = horizontal_bridge2
			self.v1 = vertical_bridge1
			self.v2 = vertical_bridge2

	f = CNF()
	nodes = [[Node(0) for _ in range(len(field[0]))] for _ in range(len(field))] 

	def initialNode():
		number = 1
		for idx in range(len(field)):
			for jdx in range(len(field[0])):

				nodes[idx][jdx] = Node(field[idx][jdx], number, number + 1, number + 2, number + 3)
				number += 4  
				# print(nodes[idx][jdx].h1, nodes[idx][jdx].h2, nodes[idx][jdx].v1, nodes[idx][jdx].v2, nodes[idx][jdx].weight)

				# no bridge on the side 
				if idx == 0 or idx == (len(field) - 1) or jdx == 0 or (jdx == len(field[0]) - 1):
					f.extend([[-nodes[idx][jdx].h1], [-nodes[idx][jdx].h2],
                             [-nodes[idx][jdx].v1], [-nodes[idx][jdx].v2]])
					
		return nodes

	nodes = initialNode() 

	def buildConstraints():
		for idx in range(1, len(field) - 1):
			for jdx in range(1, len(field[0]) - 1):
				
				if nodes[idx][jdx].weight == 0:

					# one node can not have multiple types of bridges 
					f.extend([
						[-nodes[idx][jdx].h1, -nodes[idx][jdx].v1], [-nodes[idx][jdx].h2, -nodes[idx][jdx].v2], 
						[-nodes[idx][jdx].h1, -nodes[idx][jdx].v2], [-nodes[idx][jdx].h1, -nodes[idx][jdx].h2], 
						[-nodes[idx][jdx].v1, -nodes[idx][jdx].v2], [-nodes[idx][jdx].h2, -nodes[idx][jdx].v1]
					])
					

					f.extend([
						[-nodes[idx][jdx].v1, nodes[idx - 1][jdx].v1], 
						[-nodes[idx][jdx].v2, nodes[idx - 1][jdx].v2]
					])

					f.extend([
						[-nodes[idx][jdx].v1, nodes[idx + 1][jdx].v1],
						[-nodes[idx][jdx].v2, nodes[idx + 1][jdx].v2]
					])

					f.extend([
						[-nodes[idx][jdx].h1, nodes[idx][jdx - 1].h1], 
						[-nodes[idx][jdx].h2, nodes[idx][jdx - 1].h2]
					])

					f.extend([
						[-nodes[idx][jdx].h1, nodes[idx][jdx + 1].h1], 
						[-nodes[idx][jdx].h2, nodes[idx][jdx + 1].h2]
					])

				else:
					f.extend([
						[nodes[idx][jdx].h1], [nodes[idx][jdx].v1],
						[nodes[idx][jdx].h2], [nodes[idx][jdx].v2]
					])

					

					degreeClauses = bridge_sum[nodes[idx][jdx].weight]

					mapping = {}
					mapping[1] = nodes[idx-1][jdx].v1
					mapping[2] = nodes[idx-1][jdx].v2
					mapping[3] = nodes[idx+1][jdx].v1
					mapping[4] = nodes[idx+1][jdx].v2
					mapping[5] = nodes[idx][jdx-1].h1
					mapping[6] = nodes[idx][jdx-1].h2
					mapping[7] = nodes[idx][jdx+1].h1
					mapping[8] = nodes[idx][jdx+1].h2
					
					resolve = []
					for clause in degreeClauses:
						resolve_clause = []
						for item in clause:
							mapvar = mapping[abs(item)]
							mapvar = int(math.copysign(1, item)) * mapvar
							resolve_clause.append(mapvar)

						resolve.append(resolve_clause)

					f.extend(resolve)

	buildConstraints()

	def dimacs(cnf, path):
		with open(path, 'w') as fin:
			fin.write('p cnf {} {}\n'.format(len(cnf), 4 * len(field) * len(field[0])))
			for clause in cnf:
				clause_str = ' '.join(str(item) for item in clause)
				fin.write(clause_str + ' 0\n')
	output_folder = os.path.join(os.getcwd(), 'DIMACS')

	filePath = os.path.join(output_folder, f'test-{number}.cnf')
	dimacs(f.clauses, filePath)

	return nodes, f

