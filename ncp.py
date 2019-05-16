
def initBoard(size, board):
	for i in range(size):
		for j in range(size):
			if(i == 0 or j == 0 or i == size-1 or j == size-1):
				board[i][j] = 9;
			else:
				board[i][j] = 0;

def printBoard(size, board):
	for i in range(size):
		for j in range(size):
			print (board[i][j],  " ", end="")
		print () 

def printStack(size, stack):
	print("stack: ", end=" ");
	for i in range(size):
		print(stack[i], end= " ")
	print()

def printCands(size, cands):
	for i in range(size):
		for j in range(size):
			print(cands[i][j], end= " ")
		print()

def initStack(size, stack):
	for i in range(size+2):
		stack[i] = 0 

def initCands(size, cands):
	for i in range(size):
		for j in range(size):
			cands[i][j] = -1

def isInitialBoardValid(size, board, iS, initials):
	for i in range(iS):
		row = initials[i][0];
		col = initials[i][1];
		if(canPlace(size, board, row, col) == True):
			board[row][col] = 1;
		else:
			return False;
	return True;

def canPlace(size, board, sI, col):
	i = 1
	for i in range(size-1): # check row
		if(board[sI][i] == 1):
			return False

	i = 1
	for i in range(size-1): # check col
		if(board[i][col] == 1):
			return False;

	if(sI-2 > 0 and col-1 > 0 and board[sI-2][col-1] == 1):
		return False;	

	if(sI-2 > 0 and col+1 < size-1 and board[sI-2][col+1] == 1):
		return False;	

	if(sI+2 < size-1 and col-1 > 0 and board[sI+2][col-1] == 1):
		return False;	

	if(sI+2 < size-1 and col+1 > 0 and board[sI+2][col+1] == 1):
		return False;	

	if(sI-1 > 0 and col-2 > 0 and board[sI-1][col-2] == 1):
		return False;	

	if(sI-1 > 0 and col+2 < size-1 and board[sI-1][col+2] == 1):
		return False;	

	if(sI+1 < size-1 and col-2 > 0 and board[sI+1][col-2] == 1):
		return False;	

	if(sI+1 < size-1 and col+2 < size-1 and board[sI+1][col+2] == 1):
		return False;	

	return True;

def isInitial(sI, iS, initials):
	for i in range(iS):
		if(sI == initials[i][0]):
			return True
	return False

def searchInitial(sI, iS, initials):
	for i in range(iS):
		if(sI == initials[i][0]):
			return initials[i][1]

def nchancellors(size, board, stack, cands, iS, initials):
	solution_list = []
	solution = 0
	sI = start = 0

	stack[start] = 1

	while(stack[start] > 0):
		if(sI == size+1): # soln found
			solution = solution + 1
			print("-------------------------------:");
			print("solution: ", solution)

			sol = []
			for i in range(1, size+1, 1):
				print(i, ", ", cands[i][stack[i]])
				s = []
				s.append(i)
				s.append(cands[i][stack[i]])
				sol.append(s)
				print(i, " ", cands[i][stack[i]])

			solution_list.append(sol)
			

			print("-------------------------------:");

		if(stack[sI] > 0): # get next row
			if(sI != 0):
				board[sI][cands[sI][stack[sI]]] = 1

			sI = sI + 1
			if(isInitial(sI, iS, initials) == False):
				stack[sI] = 0 

				for col in range(size, 0, -1):
					if(canPlace(size+2, board, sI, col) == True):
						stack[sI] = stack[sI] + 1
						cands[sI][stack[sI]] = col			
			else:
				stack[sI] = 1

				col = searchInitial(sI, iS, initials)
				cands[sI][stack[sI]] = col
		else: # pop
			sI = sI - 1;
			if(isInitial(sI, iS, initials) == True):
				sI = sI - 1
				board[sI][cands[sI][stack[sI]]] = 0
				stack[sI] = stack[sI] - 1
				continue
			
			board[sI][cands[sI][stack[sI]]] = 0
			stack[sI] = stack[sI] - 1

		# print("sI: ", sI); 
		# printBoard(size+2, board);
		# printStack(size+2, stack);
		# printCands(size+2, cands);


	if(stack[start] == 0 and solution == 0):
		print("No solutions");
		# board[p]["solutions"].append([]);

	return solution_list

# converts coordinates to board states, for displaying in UI
def toBoardStates(lst, size):
	solutions = []

	for sol in lst:
		solution = [[0 for j in range(size)] for i in range(size)]
		for pnt in sol:
			r = pnt[0] - 1
			c = pnt[1] - 1
			solution[r][c]  = 1
			print(solution)
		solutions.append(solution)

	return solutions

# main function
def solve(b):
	size = b['size']
	board = [[0] * (size+2) for i in range(size+2)]
	stack = [0] * (size+2)
	cands = [[0] * (size+2) for i in range(size+2)]

	initBoard(size+2, board)
	initStack(size, stack)
	initCands(size+2, board)
	
	maxInitials = size*size

	initials = [[0] * (2) for q in range(maxInitials)]
	iS = 0
	val = 0

	# get the initial points
	for x in range(size):
		for y in range(size):
			val = b['board'][x][y]
			if(val == 1):
				initials[iS][0] = x+1   # row of initial (plus 1 because it is not 0-indexing)
				initials[iS][1] = y+1   # col
				iS = iS + 1

	if(isInitialBoardValid(size+2, board, iS, initials) == True):  # check if the initial board is valid(constraints when placing a chancellor)
		solutions = nchancellors(size, board, stack, cands, iS, initials)  # call the nchancellors algo
		solutions = toBoardStates(solutions, size)
		b['solutions'] = solutions
