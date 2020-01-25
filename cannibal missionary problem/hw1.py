# Group Members
# Nogay Evirgen
# Engin Deniz Kopan
# Mehmet Ege Acıcan
# Gökçe Sefa
# Alper Mehmet Özdemir


def solver(openStates, closedStates, finalState, falsePaths):	
	
	print("format of the states are like this")
	print("abXcd")
	print("a : the number of missionaires at left side")
	print("b : the number of cannibals at left side")
	print("X : shows the location of the boat. L if left, R if right.")
	print("d : the number of missionaires at right side")
	print("e : the number of cannibals at right side")
	print("--- DFS search begins ---")
	while openStates:
		
		# openStates's format is something like this
		# [xxLyy-xxRyy-xxLyy, xxLyy-xxRyy-xxLyy-xxRyy]
		# list contains path strings.

		# currentState gets the path, and its last visited state.
		# search algorithm is DFS, followed the pseudocode from the book
		currentState = openStates[0][len(openStates[0]) - 5 : ]
		leftHuman = int(currentState[0])
		leftCannibal = int(currentState[1])
		boatDirection = currentState[2]
		rightHuman = int(currentState[3])
		rightCannibal = int(currentState[4])
		print("current path is : " +openStates[0])

		curState = openStates.pop(0)
		closedStates.append(currentState)

		# this booleans purpose is to follow false paths.
		truePath = False

		# appendedStates is a list which will get all possible next states from the current state.
		appendedStates = []

		# boat is at the left side
		if boatDirection == "L":
			# first possibility, send 1 human
			# in order to send a human, first you need to have a human.
			# after that you should check the number of cannibals-humans.
			# number of cannibals cant be higher than humans in any case.
			# but you need to remember that 0 is also a number, number of humans can be 0 while number of cannibals is 1-2-3-4-...
			# if rightHuman + rightCannibal != 0 is for a special case. If only a human/cannibal goes to an empty island, that creature has to come back since boat needs to come back. It'll be a loop.
			if leftHuman > 0:
				if leftCannibal <= leftHuman - 1 or leftHuman == 1:
					if rightHuman + 1 >= rightCannibal:
						if rightHuman + rightCannibal != 0:
							nextState = str(leftHuman - 1) + str(leftCannibal) + "R" + str(rightHuman + 1) + str(rightCannibal)

							if nextState == finalState:
								return curState + "-" + nextState , falsePaths

							if not nextState in closedStates:
								truePath = True
								appendedStates.append(curState + "-" + nextState)

			# second possibility , send 1 cannibal
			# in order to send a cannibal, first you need to have a cannibal.
			# gotta check the # of cannibals and # of humans if they prevent any condition.
			# # of humans at the right side can be 0 (again, same thing.)
			if leftCannibal > 0:
				if rightCannibal + 1 <= rightHuman or rightHuman == 0:
					if rightHuman + rightCannibal != 0:
						nextState = str(leftHuman) + str(leftCannibal - 1) +"R" + str(rightHuman) + str(rightCannibal + 1)
						if nextState == finalState:
							return curState + "-" + nextState , falsePaths

						if not nextState in closedStates:
							truePath = True
							appendedStates.append(curState + "-" + nextState)




			# third possibility, send 1 human, 1 cannibal
			# you need to have at least 1 human, 1 cannibal to send it.
			# remember that right side could have 0 human - 1 cannibal. so you gotta check the # of cannibals - humans before you send it.
			if leftHuman > 0 and leftCannibal > 0:
				if rightHuman + 1 >= rightCannibal + 1:
					nextState = str(leftHuman - 1) + str(leftCannibal - 1) + "R" + str(rightHuman + 1) + str(rightCannibal + 1)
					if nextState == finalState:
							return curState + "-" + nextState , falsePaths

					if not nextState in closedStates:
						truePath = True
						appendedStates.append(curState + "-" + nextState)



			# fourh possibility, send 2 humans
			# you need to have at least 2 humans.
			# after that you should check the number of cannibals-humans.
			# number of cannibals cant be higher than humans in any case.
			# but you need to remember that 0 is also a number, number of humans can be 0 while number of cannibals is 1-2-3-4-...
			if leftHuman > 1:
				if leftCannibal <= leftHuman - 2 or leftHuman == 2:	
					if rightHuman + 2 >= rightCannibal:	
						nextState = str(leftHuman - 2) + str(leftCannibal) + "R" + str(rightHuman + 2) + str(rightCannibal)
						if nextState == finalState:
							return curState + "-" + nextState , falsePaths
					
						if not nextState in closedStates:
							truePath = True
							appendedStates.append(curState + "-" + nextState)



			# fifth possibility , send 2 cannibal
			# you need at least 2 cannibals in order to send 2.
			# gotta check the # of cannibals and # of humans if they prevent any condition.
			# # of humans at the right side can be 0 (again, same thing.)
			if leftCannibal > 1:
				if rightCannibal + 2 <= rightHuman or rightHuman == 0:
					
					nextState = str(leftHuman) + str(leftCannibal - 2) +"R" + str(rightHuman) + str(rightCannibal + 2)
					if nextState == finalState:
						return curState + "-" + nextState , falsePaths

					if not nextState in closedStates:
						truePath = True
						appendedStates.append(curState + "-" + nextState)			

		# right side is the same as left side.
		# just switch every left to right, right to left.
		else:

			# first possibility , send 1 human
			if rightHuman > 0:
				if rightCannibal <= rightHuman - 1 or rightHuman == 1:	
					if leftHuman + 1 >= leftCannibal:
						if leftHuman + leftCannibal != 0:
							nextState = str(leftHuman + 1) + str(leftCannibal) + "L" + str(rightHuman - 1) + str(rightCannibal)
							if nextState == finalState:
								return curState + "-" + nextState , falsePaths

					
							if not nextState in closedStates:
								truePath = True
								appendedStates.append(curState + "-" + nextState)


			
			# second possibility, send 1 cannibal
			if rightCannibal > 0:
				if leftCannibal + 1 <= leftHuman or leftHuman == 0:		
					if leftHuman + leftCannibal != 0:			
						nextState = str(leftHuman) + str(leftCannibal + 1) + "L" + str(rightHuman) + str(rightCannibal - 1)
						if nextState == finalState:
							return curState + "-" + nextState , falsePaths

						
						if not nextState in closedStates:
							truePath = True
							appendedStates.append(curState + "-" + nextState)



			# third possibility, send 1 cannibal, send 1 human
			if rightCannibal > 0 and rightHuman > 0:
				if leftHuman + 1 >=  leftCannibal + 1:
					nextState = str(leftHuman + 1) + str(leftCannibal + 1) + "L" + str(rightHuman - 1) + str(rightCannibal - 1)
					if nextState == finalState:
						return curState + "-" + nextState , falsePaths
					
					if not nextState in closedStates:
						truePath = True
						appendedStates.append(curState + "-" + nextState)



			# fourth possibility, send 2 humans
			if rightHuman > 1:
				if rightCannibal <= rightHuman - 2 or rightHuman == 2:			
					if leftHuman + 2 >= leftCannibal:		
						nextState = str(leftHuman + 2) + str(leftCannibal) + "L" + str(rightHuman - 2) + str(rightCannibal)
						if nextState == finalState:
							return curState + "-" + nextState , falsePaths

						if not nextState in closedStates:
							truePath = True
							appendedStates.append(curState + "-" + nextState)


			# fifth possibility , send 2 cannibals
			if rightCannibal > 1:
				if leftCannibal + 2 <= leftHuman or leftHuman == 0:					
					nextState = str(leftHuman) + str(leftCannibal + 2) + "L" + str(rightHuman) + str(rightCannibal - 2)
					if nextState == finalState:
						return curState + "-" + nextState , falsePaths

					if not nextState in closedStates:
						truePath = True
						appendedStates.append(curState + "-" + nextState)

		# append all the appendedStates to the openStates
		if appendedStates:
			openStates[0:0] = appendedStates

		if not truePath:
			falsePaths.append(curState)


	
	return "no solution.", falsePaths





openStates = ["33L00"]
closedStates = []
falsePaths = []
finalState = "00R33"
path, falsePaths = solver(openStates, closedStates, finalState, falsePaths)
print("---search is done.---")
print("##################")
print("solution path : " + path)
print("##################")
print("All wrong paths that are searched: " )
for i in range(len(falsePaths)):
	print("Path #" + str(i + 1) + ": " + falsePaths[i])
print("################")
print("end of program.")
