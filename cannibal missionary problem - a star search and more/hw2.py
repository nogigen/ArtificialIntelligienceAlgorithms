# Group Members
# Nogay Evirgen
# Engin Deniz Kopan
# Mehmet Ege Acıcan
# Gökçe Sefa
# Alper Mehmet Özdemir

# problem : x number of missionaries and y number of cannibals should cross a river. There is a boat capacity. When the number of cannibals exceed the number of missionaries in one side, cannibals will kill missionaries.
# Find a path so that both cannibals and missionaries accross the river
# part a : find a shortest path if theres any
# part b : find the number of shortest paths if theres any.


 # heuristic stragety for part a is : minimum number of states to reach a goal from the current distance can be calculated by (missionary number of left side + cannibal number of left side) divided by the boat capacity and get floor of that value.

 # in part b , I used an oracle value which is calculated with A* . Then used DFS to find all shortest paths.

import math

# returns heuristic value of a state
# meaning its optimistic distance to the goal.
def heuristicValueCalculator(state, boatCapacity):
	leftMissionary = int(state[0])
	leftCannibal = int(state[1])
	return int(math.floor( (leftMissionary + leftCannibal) // boatCapacity))

# assuming states format is XXXXX-YYYYY-CCCCC
# returns 3
def stateLengthCalculator(path):
	return len(path.split("-"))

# sort path list with heuristics.
def sortWithHeuristics(openPaths, boatCapacity):
	totalLength = []
	for path in openPaths:
		lastState = path[len(path) - 5 : ]
		totalLength.append(stateLengthCalculator(path) + heuristicValueCalculator(lastState , boatCapacity))

	# totalLength and openPaths are parallel lists.
	# selection sort
	count = 0
	for i in range(len(totalLength)):
		min_id = i
		for j in range(i + 1 , len(totalLength)):
			if totalLength[min_id] > totalLength[j]:
				min_id = j
		if i != min_id:
			count = count + 1
		totalLength[i] , totalLength[min_id] = totalLength[min_id] , totalLength[i]
		openPaths[i] , openPaths[min_id] = openPaths[min_id] , openPaths[i]
	return count

def indexOfPathWithSearchedState(openPaths, state):
	for i in range(len(openPaths)):
		path = openPaths[i]
		if state in path.split("-"):
			return i
	return -1

# checks whether the new state will cause a loop or not.
def isLoop(path , newState):
	if newState in path.split("-"):
		return True
	else:
		return False

# show what happened between states.
# path format is aBRde-abLde
# output is like this :
# SEND    4 CANNIBALS 0 MISSIONARIES
# CC					CCCC
# MMMMMM				
# RETURN    1 CANNIBALS 0 MISSIONARIES
# CCC					CCC
# MMMMMM				
def printifyPath(path):
	print("------ start -----")
	states = path.split("-")
	missionaryNumber = int(states[0][0])
	cannibalNumber = int(states[0][1])

	# print path
	print("C" * cannibalNumber)
	print("M" * missionaryNumber)
	print()

	for i in range(len(states) - 1):
		curState = states[i]
		nextState = states[i + 1]

		leftMissionary = int(curState[0])
		leftCannibal = int(curState[1])
		boatDirection = curState[2]
		rightMissionary = int(curState[3])
		rightCannibal = int(curState[4])

		nextLeftMissionary = int(nextState[0])
		nextLeftCannibal = int(nextState[1])
		nextRightMissionary = int(nextState[3])
		nextRightCannibal = int(nextState[4])

		if boatDirection == "L":
			missionaryDifference = nextRightMissionary - rightMissionary
			cannibalDifference = nextRightCannibal - rightCannibal
		else:
			missionaryDifference = nextLeftMissionary - leftMissionary
			cannibalDifference = nextLeftCannibal - leftCannibal

		if boatDirection == "L":
			print("SEND    " + str(cannibalDifference) + " CANNIBALS " + str(missionaryDifference) + " MISSIONARIES")
		else:
			print("RETURN    " + str(cannibalDifference) + " CANNIBALS " + str(missionaryDifference) + " MISSIONARIES")

		print("C" * nextLeftCannibal + "\t" +"\t" +"\t" + "\t" + "\t" + "C" * nextRightCannibal)
		print("M" * nextLeftMissionary + "\t" + "\t" +"\t" + "\t" + "\t" + "M" * nextRightMissionary)
		print()
	print("----- end ------")



# this function is for part A
# param1 : number of missionaries
# param2 : number of cannibals
# param3 : number of boat capacity.
# param4 : initial state
# param5 : final state state
# A* search to find shortest path.
def A_starSearch(missionaryNumber, cannibalNumber, boatCapacity, initialState, finalState):
	options = []
	# filling all the possible moves to a list.
	# (number of missionary, number of cannibal) the boat can take.
	# assuming missionary and cannibal number is always greater than boat capacity.
	# if it wasnt, it wouldnt be a good problem :)

	for missionary in range(boatCapacity):
		options.append( (missionary + 1 , 0) )

	for cannibal in range(boatCapacity):
		options.append( (0 , cannibal + 1) )

	for i in range(boatCapacity // 2):
		options.append( (i + 1 , i + 1) )

	for missionary in range(boatCapacity):
		for cannibal in range(boatCapacity // 2):
			numMissionary = missionary + 1
			numCannibal = cannibal + 1
			if numMissionary > numCannibal:
				if numMissionary + numCannibal <= boatCapacity:
					if (numMissionary , numCannibal) not in options:
						options.append( (numMissionary , numCannibal) )

	
	openPaths = [initialState]
	# keys -> states
	# values -> number of states to visit to go to that state in the shortest path.
	minLen_toStates = {initialState : 0}
	counter = 0
	while openPaths:
		print(openPaths)
		# openStates[0] is a path, its last 5 character shows the last state.
		currentState = openPaths[0][len(openPaths[0]) - 5 : ]
		currentPath = openPaths.pop(0)

		if currentState == finalState:
			return currentPath
		
		leftMissionary = int(currentState[0]) 			
		leftCannibal = int(currentState[1])
		boatDirection = currentState[2]
		rightMissionary = int(currentState[3]) 			
		rightCannibal = int(currentState[4]) 
		
		# try all possible moves.
		for option in options:
			boatMissionary = option[0]
			boatCannibal = option[1]

			# check whether the options meets the conditions
			# if boat is at the left side
			if boatDirection == "L":
				if leftMissionary >= boatMissionary and leftCannibal >= boatCannibal:
					if leftMissionary - boatMissionary >= leftCannibal - boatCannibal or leftMissionary - boatMissionary == 0:
						if rightMissionary + boatMissionary >= rightCannibal + boatCannibal or rightMissionary + boatMissionary == 0:
							nextState = str(leftMissionary - boatMissionary) + str(leftCannibal - boatCannibal) + str("R") + str(rightMissionary + boatMissionary) + str(rightCannibal + boatCannibal)

							# check if path becomes a loop or not.
							if not isLoop(currentPath, nextState):
								# check if that state is reached before or not.
								if nextState in minLen_toStates:
									# check whether we found a shorter path from Start to this current state or not.
									if minLen_toStates[nextState] > stateLengthCalculator(currentPath):
										minLen_toStates[nextState] = stateLengthCalculator(currentPath)
										openPaths.pop(indexOfPathWithSearchedState(openPaths , nextState))
										openPaths.append(currentPath + "-" + nextState)			

									# not necessary since we are only looking for 1 shortest path.
									# elif minLen_toStates[nextState] == stateLengthCalculator(currentPath):		
									# 	openPaths.append(currentPath + "-" + nextState)	
								else:
									minLen_toStates[nextState] = stateLengthCalculator(currentPath)
									openPaths.append(currentPath + "-" + nextState)
									

			# if boat is at the right side.
			else:
				if rightMissionary >= boatMissionary and rightCannibal >= boatCannibal:
					if (rightMissionary - boatMissionary >=  rightCannibal - boatCannibal) or (rightMissionary - boatMissionary) == 0:
						if (leftMissionary + boatMissionary >= leftCannibal + boatCannibal) or (leftMissionary + boatMissionary) == 0:
							nextState = str(leftMissionary + boatMissionary) + str(leftCannibal + boatCannibal) + str("L") + str(rightMissionary - boatMissionary) + str(rightCannibal - boatCannibal)

							if not isLoop(currentPath, nextState):
								if nextState in minLen_toStates:
									if minLen_toStates[nextState] > stateLengthCalculator(currentPath):
										minLen_toStates[nextState] = stateLengthCalculator(currentPath)									
										openPaths.pop(indexOfPathWithSearchedState(openPaths , nextState))
										openPaths.append(currentPath + "-" + nextState)		

									# not necessary since we are only looking for 1 shortest path.
									# elif minLen_toStates[nextState] == stateLengthCalculator(currentPath):		
									# 	openPaths.append(currentPath + "-" + nextState)

								else:
									minLen_toStates[nextState] = stateLengthCalculator(currentPath)
									openPaths.append(currentPath + "-" + nextState)


		# sort the openPaths list considering heuristics.
		counter = sortWithHeuristics(openPaths , boatCapacity) + counter

	print("no solution")
	return None


# this function is for part B
# param1 : number of missionaries
# param2 : number of cannibals
# param3 : boat capacity
# param4 : initial state
# param5 : final state state
# param6 : length of the shortest path. (oracle)

# DFS to find all shortest paths.
def DFSwithOracleForAllShortestPaths(missionaryNumber, cannibalNumber, boatCapacity, initialState, finalState, oracle):
	options = []
	for missionary in range(boatCapacity):
		options.append( (missionary + 1 , 0) )

	for cannibal in range(boatCapacity):
		options.append( (0 , cannibal + 1) )

	for i in range(boatCapacity // 2):
		options.append( (i + 1 , i + 1) )

	for missionary in range(boatCapacity):
		for cannibal in range(boatCapacity // 2):
			numMissionary = missionary + 1
			numCannibal = cannibal + 1
			if numMissionary > numCannibal:
				if numMissionary + numCannibal <= boatCapacity:
					if (numMissionary , numCannibal) not in options:
						options.append( (numMissionary , numCannibal) )
	
	openPaths = [initialState]
	all_shortest_paths = []
	minLen_toStates = {initialState : 0}
	while openPaths:
		print(openPaths)
		currentState = openPaths[0][len(openPaths[0]) - 5 : ]
		currentPath = openPaths.pop(0)

		if oracle >= stateLengthCalculator(currentPath):

			if currentState == finalState:
				all_shortest_paths.append(currentPath)
			
			leftMissionary = int(currentState[0]) 			
			leftCannibal = int(currentState[1])
			boatDirection = currentState[2]
			rightMissionary = int(currentState[3]) 			
			rightCannibal = int(currentState[4]) 

			
			for option in options:
				boatMissionary = option[0]
				boatCannibal = option[1]

				if boatDirection == "L":
					if leftMissionary >= boatMissionary and leftCannibal >= boatCannibal:
						if leftMissionary - boatMissionary >= leftCannibal - boatCannibal or leftMissionary - boatMissionary == 0:
							if rightMissionary + boatMissionary >= rightCannibal + boatCannibal or rightMissionary + boatMissionary == 0:
								nextState = str(leftMissionary - boatMissionary) + str(leftCannibal - boatCannibal) + str("R") + str(rightMissionary + boatMissionary) + str(rightCannibal + boatCannibal)

								if not isLoop(currentPath, nextState):
									if nextState in minLen_toStates:
										if minLen_toStates[nextState] > stateLengthCalculator(currentPath):
											minLen_toStates[nextState] = stateLengthCalculator(currentPath)
											index = indexOfPathWithSearchedState(openPaths , nextState)
											if index != -1:
												openPaths.pop(indexOfPathWithSearchedState(openPaths , nextState))
											openPaths[0:0] = [currentPath + "-" + nextState]

										elif minLen_toStates[nextState] == stateLengthCalculator(currentPath):		
											openPaths[0:0] = [currentPath + "-" + nextState]					

									else:
										minLen_toStates[nextState] = stateLengthCalculator(currentPath)
										openPaths[0:0] = [currentPath + "-" + nextState]
										


				else:
					if rightMissionary >= boatMissionary and rightCannibal >= boatCannibal:
						if (rightMissionary - boatMissionary >=  rightCannibal - boatCannibal) or (rightMissionary - boatMissionary) == 0:
							if (leftMissionary + boatMissionary >= leftCannibal + boatCannibal) or (leftMissionary + boatMissionary) == 0:
								nextState = str(leftMissionary + boatMissionary) + str(leftCannibal + boatCannibal) + str("L") + str(rightMissionary - boatMissionary) + str(rightCannibal - boatCannibal)

								if not isLoop(currentPath, nextState):
									if nextState in minLen_toStates:
										if minLen_toStates[nextState] > stateLengthCalculator(currentPath):
											minLen_toStates[nextState] = stateLengthCalculator(currentPath)									
											index = indexOfPathWithSearchedState(openPaths , nextState)
											if index != -1:
												openPaths.pop(indexOfPathWithSearchedState(openPaths , nextState))
											openPaths[0:0] = [currentPath + "-" + nextState]	

										elif minLen_toStates[nextState] == stateLengthCalculator(currentPath):		
											openPaths[0:0] = [currentPath + "-" + nextState]

									else:
										minLen_toStates[nextState] = stateLengthCalculator(currentPath)
										openPaths[0:0] = [currentPath + "-" + nextState]

	return all_shortest_paths


print("format of the states are like this : abcde")
print("a -> is the number of missionary on the left side")
print("b -> is the number of cannibal on the left side")
print("c -> is where the boat is, its L (left) or R (right)")
print("d -> is the number of missionary on the right side")
print("e -> is the number of cannibal on the right side")


# part A of homework2
print("------ part A begins ------")
shortest_path = A_starSearch(6,6,5,"66L00","00R66")
if shortest_path:
	print("shortest path : " +shortest_path)
else:
	print("no path.")
printifyPath(shortest_path)
print("------ part A ends ------")
print("--------------------------")
print("--------------------------")


# part B of homework2
print("------ part B begins ------")
print("---- searching for oracle value -----")
oraclePath = A_starSearch(4,4,3,"44L00", "00R44")
print("---- oracle value found ----")
print("---------------")
oracle = stateLengthCalculator(oraclePath)
print("----- DFS begins -----")
all_shortest_paths = DFSwithOracleForAllShortestPaths(4,4,3,"44L00","00R44",oracle)
print("---- DFS ends ----")
print("---------------")
print("---------------")
print("number of shortest paths is : " +str(len(all_shortest_paths)))
print("---------------")
print("---------------")
print("---- all the shortest paths are down below ----------")
print(all_shortest_paths)
print("------ part B ends ------")

