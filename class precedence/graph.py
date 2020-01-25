# a graph
class Graph:
	def __init__(self):
		self.nodes = {}

	# add a node to graph
	def addNode(self, node):
		if node in self.nodes:
			print("a node with this class already exists.")
		else:
			self.nodes[node.name] = node

	# from node1 to node2.
	def addEdge(self, node1, node2):
		self.nodes[node1.name].adjacents.append(node2)