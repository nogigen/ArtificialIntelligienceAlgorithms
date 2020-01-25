# Group Members
# Alper Mehmet Özdemir
# Gökçe Sefa
# Nogay Evirgen
# Engin Deniz Kopan
# Mehmet Ege Acıcan

import sys
# a Node presents a board state (kind of)
class Node:
	def __init__(self, board):
		self.board = board
		self.bestChildren = None
		self.setMaximizingPlayer()
		self.childrens = []
	# decides who's turn is it.
	def setMaximizingPlayer(self):
		squares = self.board.split("-")
		x_count = 0
		o_count = 0
		for square in squares:
			if square == "X":
				x_count += 1
			elif square == "O":
				o_count += 1
		if x_count == o_count:
			self.maximizingPlayer = True
		else:
			self.maximizingPlayer = False

	# branches and creates new nodes.
	def branch(self):
		branches = []
		squares = self.board.split("-")
		if self.maximizingPlayer:
			for i in range(len(squares)):
				if squares[i] == "_":
					newBoard = self.board[0: i * 2] + "X" + self.board[i * 2 + 1 :]
					child = Node(newBoard)
					branches.append(child)
		else:
			for i in range(len(squares)):
				if squares[i] == "_":
					newBoard = self.board[0: i * 2] + "O" + self.board[i * 2 + 1 :]
					child = Node(newBoard)
					branches.append(child)
		self.childrens = branches
		return branches

# return value of the board.
def static_evaluator(board):
	if X_Won(board):
		return 1
	elif O_Won(board):
		return -1
	else:
		return 0

# returns true if X won the game.
# return false if not
def X_Won(board):
	squares = board.split("-")
	for i in range(3):
		if squares[i * 3] == "X" and squares[i * 3 + 1] == "X" and squares[i * 3 + 2] == "X":
			return True
	for i in range(3):
		if squares[i] == "X" and squares[i + 3 * 1] == "X" and squares[i + 3 * 2] == "X":
			return True
	if (squares[0] == "X" and squares[4] == "X" and squares[8] == "X") or (squares[2] == "X" and squares[4] == "X" and squares[6] == "X"):
		return True
	return False

# return true if O won the game.
# return false if not.
def O_Won(board):
	squares = board.split("-")
	for i in range(3):
		if squares[i * 3] == "O" and squares[i * 3 + 1] == "O" and squares[i * 3 + 2] == "O":
			return True
	for i in range(3):
		if squares[i] == "O" and squares[i + 3 * 1] == "O" and squares[i + 3 * 2] == "O":
			return True
	if (squares[0] == "O" and squares[4] == "O" and squares[8] == "O") or (squares[2] == "O" and squares[4] == "O" and squares[6] == "O"):
		return True
	return False

# returns true if its a draw.
# returns false if not
def isDraw(board):
	if not X_Won(board) and not O_Won(board):
		if "_" not in board:
			return True
	return False

# returns true if game is over.
# returns false if not.
def isGameOver(board):
	if X_Won(board) or O_Won(board) or isDraw(board):
		return True
	return False

# 1-2-3-4-5-6-7-8-9
# 1 | 2 | 3
# 4 | 5 | 6
# 7 | 8 | 9
# displays the board like above.
def displayBoard(board):
	squares = board.split("-")
	string = ""
	for i in range(3):
		if i != 2:
			string = string + squares[i * 3] + " | " + squares[i * 3 + 1] + " | " + squares[i * 3 + 2] +"\n" 
		else:
			string = string + squares[i * 3] + " | " + squares[i * 3 + 1] + " | " + squares[i * 3 + 2]
	return string

# alpha beta pruning to make the best move.
def alpha_beta_pruning(node, alpha, beta):
	print(node.board)
	board = node.board
	if isGameOver(board):
		return static_evaluator(board)

	if node.maximizingPlayer:
		maxValue = -sys.maxsize - 1
		childrens = node.branch()
		for child in childrens:
			value = alpha_beta_pruning(child, alpha, beta)
			if value > maxValue:
				maxValue = value
				node.bestChildren = child
			alpha = max(maxValue, alpha)
			if beta <= alpha:
				break
		return maxValue
	else:
		minValue = sys.maxsize
		childrens = node.branch()
		for child in childrens:
			value = alpha_beta_pruning(child, alpha, beta)
			if value < minValue:
				minValue = value
				node.bestChildren = child
			beta = min(minValue, beta)
			if beta <= alpha:
				break
		return minValue



# main function.
# you can change the variable empty_board to see other outcomes.. its 8 lines below.
def main():
	print("please be careful to not miss the solutions. while scrolling down.")
	# 1-2-3-4-5-6-7-8-9
	# 1 | 2 | 3
	# 4 | 5 | 6
	# 7 | 8 | 9
	# you can change this empty_board variable to see other outcomes.
	empty_board = "_-_-_-_-_-_-_-_-_"
	root = Node(empty_board)
	print("evaluating the best move for game1.")
	game_value = alpha_beta_pruning(root, -sys.maxsize -1, sys.maxsize)
	print("search is done.")
	# print the whole game
	
	print("game1 starts with this board.")
	print(displayBoard(root.board))
	print("value of the board is : " +str(game_value))
	print()
	node = root.bestChildren
	while node:
		# print statements are delayed for 1 move, since i showed root at the beginning.
		if node.maximizingPlayer:
			print("O plays.")
		else:
			print("X plays.")
		print(displayBoard(node.board))
		print("static value is : " +str(static_evaluator(node.board)))
		child_values = []
		for child in node.childrens:
			child_values.append(static_evaluator(child.board))
		print("child values : " +str(child_values))
		print()
		node = node.bestChildren

	print("-------------------------------")
	print("-------------------------------")
	print("-------------------------------")
	if game_value == 1:
		print("X wins.")
	elif game_value == -1:
		print("O wins.")
	else:
		print("It's a draw.")

	for i in range(50):
		print("----------------------")
	
	print("new game.")
	empty_board = "X-_-_-O-_-_-_-_-_"
	root = Node(empty_board)
	print("evaluating the best move for game2.")
	game_value = alpha_beta_pruning(root, -sys.maxsize -1, sys.maxsize)
	print("search is done.")
	# print the whole game
	print("----------------------")
	print("----------------------")
	print("----------------------")
	print("game2 starts with this board. game1 (which asks to be done in the homework should be above.)")
	print(displayBoard(root.board))
	print("value of the board is : " +str(game_value))
	print()
	node = root.bestChildren
	while node:
		# print statements are delayed for 1 move, since i showed root at the beginning.
		if node.maximizingPlayer:
			print("O plays.")
		else:
			print("X plays.")
		print(displayBoard(node.board))
		print("static value is : " +str(static_evaluator(node.board)))
		for child in node.childrens:
			child_values.append(static_evaluator(child.board))
		print("child values : " +str(child_values))
		print()
		node = node.bestChildren


	if game_value == 1:
		print("X wins.")
	elif game_value == -1:
		print("O wins.")
	else:
		print("It's a draw.")

main()