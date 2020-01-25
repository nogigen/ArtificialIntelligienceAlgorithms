# Group Members
# Alper Mehmet Özdemir
# Gökçe Sefa
# Nogay Evirgen
# Engin Deniz Kopan
# Mehmet Ege Acıcan

# to deepcopy
import copy
from graph import Graph
from node import Node
from utils import g_test1, q1_g, q2_g, q3_g, node1, q1_node1, q1_node4, q2_node3, q2_node1, q2_node4, q3_node1, q3_node2, q3_node3

# calculates all the fish hook pairs in a list and returns it
def all_fish_hook_pairs(graph , class_list):
	pairs = []
	for node in graph.nodes:		
		if is_node_in_class_list(graph.nodes[node],class_list):
			adjacents = graph.nodes[node].adjacents
			# if graph.nodes[node].name == "Jacque":
			# 	print(len(graph.nodes[node].adjacents))
			if len(adjacents) == 0:
				pairs.append( (graph.nodes[node] ,) ) # tuple with 1 element
			else:
				for i in range(len(adjacents)):
					if i == 0:
						pairs.append( (graph.nodes[node],adjacents[0]) )

					else:
						pairs.append( (adjacents[i - 1] , adjacents[i]) )
	
	return pairs

# for example, in figure 9.6 -> node would be "Crazy"
# graph is graph
# returned list will be Crazy, Professors, Hackers, Eccentrics, Teachers, Programmers, Dwarfs, Everything
def get_classes_we_care(graph, node):
	classes = [node]
	adjacents = copy.deepcopy(node.adjacents)
	# while there are any adjacents
	while adjacents:
		count = 0
		removedAdjacent = adjacents.pop(0)
		for _class in classes:
				if _class.name == removedAdjacent.name:
					count += 1
		if count == 0:
			classes.append(removedAdjacent)


		for adjacent in removedAdjacent.adjacents:
			count = 0
			for _class in classes:
				if _class.name == adjacent.name:
					count += 1
			if count == 0:
				classes.append(adjacent)
				adjacents.append(adjacent)

	return classes

def is_node_in_class_list(node , class_list):
	for _class in class_list:
		if node.name == _class.name:
			return True
	return False

# finds the class precedence list.
# returns a list.
def sort_with_fish_hook_pairs(fishHookPairs):
	sorted_list = []
	tie_breaker = []
	while len(fishHookPairs) != 0 or len(tie_breaker) == 0:
		# if its the last name. just take it and break it
		# in winston's book, figure 9.6, everything is alone. For cases like that.
		# it will come here only once
		if len(fishHookPairs) == 1:
			if len(fishHookPairs[0]) == 1:
				sorted_list.append(fishHookPairs[0][0])
				return sorted_list


		for pairs in fishHookPairs:
			if len(pairs) == 2:
				left_side = pairs[0] 
				left_side_counter = 0
				for _pairs in fishHookPairs:
					if len(_pairs) == 2:
						right_side = _pairs[1]

						if left_side.name == right_side.name:
							left_side_counter += 1
							break # if there is any left side == right side, can stop searching.

				if left_side_counter == 0:
					count = 0
					for _tie_breaker in tie_breaker:
						if _tie_breaker.name == left_side.name:
							count += 1
					if count == 0:
						tie_breaker.append(left_side)

		if len(tie_breaker) == 1:
			sorted_list.append(tie_breaker[0])
			delete_exposed_pairs(tie_breaker[0], fishHookPairs)
			tie_breaker.pop(0)
		
		# tiebreaker.
		else:
			for i in range(len(sorted_list)):
				lowest_precedence = sorted_list[len(sorted_list) -1 -i]
				adjacents = lowest_precedence.adjacents

				counter = 0
				index = None
				for j in range(len(tie_breaker)):
					if tie_breaker[j] in adjacents:
						counter += 1
						index = j
				if counter == 1:
					sorted_list.append(tie_breaker[index])
					delete_exposed_pairs(tie_breaker[index], fishHookPairs)
					tie_breaker.pop(index) # pop it from tie_breaker list.
					break #tiebreaker decided, no need to continue.
	return sorted_list


# deletes exposed pairs
def delete_exposed_pairs(node, fishHookPairs):
	index = 0
	counter = 0

	while counter < len(fishHookPairs):
		pair = fishHookPairs[index]

		if len(pair) == 2:
			left_side = pair[0]
			if left_side.name == node.name:
				fishHookPairs.pop(index)
				index -= 1

		counter += 1
		index += 1

# prints class precedence list.
def printPrecedenceList(sortedNodes):
	for node in sortedNodes:
		print(node.name)



if __name__ == '__main__':	
	graphs = [g_test1, q1_g, q1_g, q2_g, q2_g, q2_g, q3_g, q3_g, q3_g]
	iteration = [1,2,3,3]
	for_classes = ["Crazy", "CAIVehicle", "CAIPlayer", "ifstream", "fstream", "ofstream", "Consultant Manager", "Director", "Permanent Manager"]
	for_classes_node = [node1, q1_node1, q1_node4, q2_node3, q2_node1, q2_node4, q3_node1, q3_node2, q3_node3]
	question_number = 1
	for i in range(9):
		if i == 0: # test
			print("Test the 9.6 figure from winston's book")
		
		if i == 1 or i == 3 or i == 6:
			print("---------------------------------------------")
			print("---------------------------------------------")
			print("---------------------------------------------")
			print("Question " +str(question_number))
			question_number += 1

		print("for the " +for_classes[i] +" class")
		class_list = get_classes_we_care(graphs[i], for_classes_node[i])
		fishHookPairs = all_fish_hook_pairs(graphs[i] , class_list)
		sorted_list = sort_with_fish_hook_pairs(fishHookPairs)
		printPrecedenceList(sorted_list)
		print("end of " +for_classes[i])
		print("--------------------")

	print("end of homework4")
	# print("Test the 9.6 figure from winston's book")
	# print("for the Crazy class")
	# class_list = get_classes_we_care(g_test1, node1)
	# fishHookPairs = all_fish_hook_pairs(g_test1 , class_list)
	# sorted_list = sort_with_fish_hook_pairs(fishHookPairs)
	# printPrecedenceList(sorted_list)



	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("Question 1")



	# print("for CAIVehicle : ")
	# q1_partA_class_list = get_classes_we_care(q1_g, q1_node1)
	# q1_partA_fishHookPairs = all_fish_hook_pairs(q1_g, q1_partA_class_list)
	# q1_partA_sorted_list = sort_with_fish_hook_pairs(q1_partA_fishHookPairs)
	# printPrecedenceList(q1_partA_sorted_list)
	# print("end of CAIVehicle")

	# print("---------------------------")

	# print("for CAIPlayer : ")
	# q1_partB_class_list = get_classes_we_care(q1_g, q1_node4)
	# q1_partB_fishHookPairs = all_fish_hook_pairs(q1_g, q1_partB_class_list)
	# q1_partB_sorted_list = sort_with_fish_hook_pairs(q1_partB_fishHookPairs)
	# printPrecedenceList(q1_partB_sorted_list)
	# print("end of CAIPlayer")

	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("Question 2")



	# print("for ifstream : ")
	# q2_partA_class_list = get_classes_we_care(q2_g, q2_node3)
	# q2_partA_fishHookPairs = all_fish_hook_pairs(q2_g, q2_partA_class_list)
	# q2_partA_sorted_list = sort_with_fish_hook_pairs(q2_partA_fishHookPairs)
	# printPrecedenceList(q2_partA_sorted_list)
	# print("end of ifstream")

	# print("-------------------------")

	# print("for fstream : ")
	# q2_partB_class_list = get_classes_we_care(q2_g, q2_node1)
	# q2_partB_fishHookPairs = all_fish_hook_pairs(q2_g, q2_partB_class_list)
	# q2_partB_sorted_list = sort_with_fish_hook_pairs(q2_partB_fishHookPairs)
	# printPrecedenceList(q2_partB_sorted_list)
	# print("end of fstream")


	# print("-------------------------")


	# print("for ofstream : ")
	# q2_partC_class_list = get_classes_we_care(q2_g, q2_node4)
	# q2_partC_fishHookPairs = all_fish_hook_pairs(q2_g, q2_partC_class_list)
	# q2_partC_sorted_list = sort_with_fish_hook_pairs(q2_partC_fishHookPairs)
	# printPrecedenceList(q2_partC_sorted_list)
	# print("end of ofstream")


	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("Question 3")



	# print("for Consultant Manager : ")
	# q3_partA_class_list = get_classes_we_care(q3_g, q3_node1)
	# q3_partA_fishHookPairs = all_fish_hook_pairs(q3_g, q3_partA_class_list)
	# q3_partA_sorted_list = sort_with_fish_hook_pairs(q3_partA_fishHookPairs)
	# printPrecedenceList(q3_partA_sorted_list)
	# print("end of Consultant Manager")


	# print("-------------------------")

	# print("for Director : ")
	# q3_partB_class_list = get_classes_we_care(q3_g, q3_node2)
	# q3_partB_fishHookPairs = all_fish_hook_pairs(q3_g, q3_partB_class_list)
	# q3_partB_sorted_list = sort_with_fish_hook_pairs(q3_partB_fishHookPairs)
	# printPrecedenceList(q3_partB_sorted_list)
	# print("end of Director")

	# print("-------------------------")

	# print("for Permanent Manager : ")
	# q3_partC_class_list = get_classes_we_care(q3_g, q3_node3)
	# q3_partC_fishHookPairs = all_fish_hook_pairs(q3_g, q3_partC_class_list)
	# q3_partC_sorted_list = sort_with_fish_hook_pairs(q3_partC_fishHookPairs)
	# printPrecedenceList(q3_partC_sorted_list)
	# print("end of Permanent Manager")

	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("---------------------------------------------")
	# print("end of homework 4")