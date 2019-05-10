from tkinter import filedialog
from tkinter import *

class NChancellorsApp(Frame):

	# indexes for showSolution method.
	# index_sol corresponds to the i-th solution to the j-th board (corresponds to index_brd)
	# index_brd corresponds to the i-th board loaded from file.
	# if board is manually entered through the program, it's always 0. 
	index_sol = 0
	index_brd = 0

	# these two are created and destroyed every function call,
	# no need to make a list of these corresponding to boards
	board_buttons = None
	board_labels= None

	# for loading file
	file_input = None

	# dictionary containing the size, board, variables and list of solutions
	# size 	<- int
	# board <- a list of lists or 2d list containing '1' (has chancellor), or '0' (blank)
	# variables <- a list of lists or 2d list containing IntVar() corresponding to board, links the board to its buttons
	# solutions <- list of board states, or solved boards.
	board = {}

	# list of Frames() as groups that contain widgets
	row = []

	def __init__ (self, parent):
		Frame.__init__(self, parent)

		# initialize widgets but don't show them yet
		self.initWidgets()
		# show the starting window
		self.startWindow()

	# hides ('forgets') static widgets and
	# destroys dynamic widgets, like board buttons
	def clearWidgets(self, to_forget=None, to_destroy=None):
		# hides the groups of the method that called it
		if to_forget != None:
			for i in to_forget:
				self.row[i].forget()

		# destroys the groups' child widgets(?)
		if to_destroy != None:
			for i in to_destroy:
				for child in self.row[i].winfo_children():
					child.destroy()
				self.row[i].forget()

	# returns a sizexsize 2d list of IntVar(),
	# for linking the buttons' texts to board state
	def initVariables(self, size):
		# initialize int variables for each button
		variables=[]
		for i in range(size):
			rows = []
			for j in range(size):
				var = IntVar()
				var.set(0)
				rows.append(var)

			variables.append(rows)

		return variables

	# here is where all static UI elements are declared
	# they will only be seen when their group (row) is 'packed'
	# the row is packed and shown along with its child widgets
	# when a method is called.
	def initWidgets(self):
		# create the rows or groups of widgets
		for i in range(7):
			self.row.append(Frame())

		# row 0; startWindow
		self.size_entry = Entry(self.row[0])
		self.size_entry.pack(fill=X, side=LEFT)

		self.size_button = Button(self.row[0], text="Enter", command=lambda:self.playBoard(to_forget=[0]))
		self.size_button.pack(fill=X, side=LEFT)
		
		self.load_button = Button(self.row[0], text="Load", command=self.loadFile)
		self.load_button.pack(fill=X, side=LEFT)

		# row 1 is for dynamically created board (playBoard)

		# row 2; playBoard
		self.solve_button = Button(self.row[2], text="Solve", command=lambda:self.showBoard(self.index_brd, self.index_sol, to_forget=[0,2], to_destroy=[1], solve=True))
		self.solve_button.pack(fill=X, side=RIGHT)

		self.back_button = Button(self.row[2], text="Back", command=lambda:self.startWindow(to_forget=[0,2], to_destroy=[1]))
		self.back_button.pack(fill=X, side=LEFT)

		# row 3 is for dynamically created board (showSolutions)

		# row 4; showSolutions
		self.sol_label = Label(self.row[4], text="Solutions")
		self.sol_label.grid(row=1, column=2)

		self.sol_prev_button = Button(self.row[4], text="<<", command=lambda:self.updateIndexes(0, -1, 2, to_forget=[4], to_destroy=[3]))
		self.sol_prev_button.grid(row=2, column=1)

		self.sol_count_var = StringVar()
		self.sol_count_label = Label(self.row[4], textvariable=self.sol_count_var)
		self.sol_count_label.grid(row=2, column=2)

		self.sol_next_button = Button(self.row[4], text=">>", command=lambda:self.updateIndexes(0, 1, 2, to_forget=[4], to_destroy=[3]))
		self.sol_next_button.grid(row=2, column=3)

		self.brd_label = Label(self.row[4], text="Boards")
		self.brd_label.grid(row=3, column=2)

		self.brd_prev_button = Button(self.row[4], text="<<", command=lambda:self.updateIndexes(-1, None, 2, to_forget=[4], to_destroy=[3]))
		self.brd_prev_button.grid(row=4, column=1)

		self.brd_count_var = StringVar()
		self.brd_count_label = Label(self.row[4], textvariable=self.brd_count_var)
		self.brd_count_label.grid(row=4, column=2)

		self.brd_next_button = Button(self.row[4], text=">>", command=lambda:self.updateIndexes(1, None, 2, to_forget=[4], to_destroy=[3]))
		self.brd_next_button.grid(row=4, column=3)

		self.again_button = Button(self.row[4], text="Restart", command=lambda:self.startWindow(to_forget=[4], to_destroy=[3]))
		self.again_button.grid(row=5, column=2)

		# row 5 is for dynamically created board (showBoard)

		# row 6; showBoard
		self.shw_next_button = Button(self.row[6], text=">>", command=lambda:self.updateIndexes(1, 0, 1, to_forget=[6], to_destroy=[5]))
		self.shw_next_button.grid(row=1, column=3)

		self.shw_brd_var = StringVar()
		self.shw_brd_label = Label(self.row[6], textvariable=self.shw_brd_var)
		self.shw_brd_label.grid(row=1, column=2)

		self.shw_prev_button = Button(self.row[6], text="<<", command=lambda:self.updateIndexes(-1, 0, 1, to_forget=[6], to_destroy=[5]))
		self.shw_prev_button.grid(row=1, column=1)

		self.shw_back_button = Button(self.row[6], text="Restart", command=lambda:self.startWindow(to_forget=[6], to_destroy=[5]))
		self.shw_back_button.grid(row=2, column=1)  

		self.shw_confirm_button = Button(self.row[6], text="Confirm", command=lambda:self.showSolutions(self.index_brd, self.index_sol, to_forget=[6], to_destroy=[5]))
		self.shw_confirm_button.grid(row=2, column=3)  

	def loadFile(self):
		self.file_input = filedialog.askopenfilename(initialdir="./", title="Select file")

		with open(self.file_input, encoding="latin-1") as file_handle:
			# load the whole file as a list of tuples
			lst = [tuple(map(int, line.split(' '))) for line in file_handle]

			# pop the number of puzzles from the list
			num = int(lst.pop(0)[0])

			# loop through each board size and board tiles,
			# pop the size, 
			# pop the row tuples by size, and 
			# append to boards list, and
			# append to board size list
			# self.board_sizes=[]
			# self.boards=[]
			self.board = {}
			for i in range(num):
				size = int(lst.pop(0)[0])
				board = [lst.pop(0) for i in range(size)]
				variables = self.initVariables(size)
				variables = self.setVariables(size, variables, board)
				self.board.update({i:{'size':size, 'board':board, 'variables':variables, 'solutions':[]}})
				# self.board_sizes.append(size)
				# self.boards.append(board)

			self.showBoard(0, 0, to_forget=[0], to_destroy=None, solve=True)

	def placeChancellor(self, i, j):
		# if self.board_strvars[i][j].get() == 0:
		# 	self.board_strvars[i][j].set(1)
		# 	self.boards[0][i][j] = 1
		# else:
		# 	self.board_strvars[i][j].set(0)
		# 	self.boards[0][i][j] = 0

		if self.board[0]['variables'][i][j].get() == 0:
			self.board[0]['variables'][i][j].set(1)
			self.board[0]['board'][i][j] = 1
		else:
			self.board[0]['variables'][i][j].set(0)
			self.board[0]['board'][i][j] = 0

		print(self.board[0]['board'])

	def playBoard(self, to_forget=None, to_destroy=None):
		self.clearWidgets(to_forget, to_destroy)
		# get the board_size from user
		# self.board_sizes = []
		# self.board_sizes.append(int(self.size_entry.get()))
		size = int(self.size_entry.get())

		# initialize board and append
		# to boards list
		board = [[0 for j in range(size)] for i in range(size)]
		# self.boards.append(board)

		variables = self.initVariables(size)

		# reset board dict
		self.board = {}
		# update board dict
		self.board.update({0:{'size':size, 'board':board, 'variables':variables, 'solutions':[]}})

		# insert list of lists of buttons here
		self.row[1].pack(fill=X)
		self.board_buttons = []
		for i in range(size):
			self.row_buttons=[]
			for j in range(size):
				self.row_buttons.append(Button(self.row[1], textvariable=self.board[0]['variables'][i][j], command=lambda i=i, j=j:self.placeChancellor(i, j), height=2, width=3))
				self.row_buttons[j].grid(row=i, column=j)

			self.board_buttons.append(self.row_buttons)

		# for solve and back button
		self.row[2].pack(fill=X)

	# sets the variables to match the board state
	def setVariables(self, size, variables_list, board_state):
		for i in range(size):
			for j in range(size):
				variables_list[i][j].set(board_state[i][j])

		return variables_list

	# this will also show the board
	def showBoard(self, index_brd, index_sol, to_forget=None, to_destroy=None, solve=False):
		if solve != False:
			# do n-chancellors problem here or 
			# do it in a separate function
			# but call it here
			self.solveNChancellorsProblem()

		self.clearWidgets(to_forget, to_destroy)

		brd_count = str(index_brd + 1) + "/ " + str(len(self.board))
		self.shw_brd_var.set(brd_count)

		# show the label group
		self.row[5].pack(fill=X)
		# reset label list
		self.board_labels = []

		# unpack dict values
		size = self.board[index_brd]['size']
		variables = self.board[index_brd]['variables']
		for i in range(size):
			self.row_labels=[]
			for j in range(size):
				self.row_labels.append(Button(self.row[5], textvariable=variables[i][j], height=2, width=3, relief=SUNKEN, state=DISABLED))
				self.row_labels[j].grid(row=i, column=j)

			self.board_labels.append(self.row_labels)

		self.row[6].pack(fill=X)

	# this will show the solutions
	def showSolutions(self, index_brd, index_sol, to_forget=None, to_destroy=None):
		self.clearWidgets(to_forget, to_destroy)

		sol_count = str(index_sol + 1) + "/ " + str(len(self.board[index_brd]['solutions']))
		self.sol_count_var.set(sol_count)

		brd_count = str(index_brd + 1) + "/ " + str(len(self.board))
		self.brd_count_var.set(brd_count)

		# show the label group
		self.row[3].pack(fill=X)
		# reset label list
		self.board_labels = []

		# unpack dict values
		# board = self.board[index_brd]['board']
		size = self.board[index_brd]['size']
		solution = self.board[index_brd]['solutions'][index_sol]
		variables = self.board[index_brd]['variables']
		variables = self.setVariables(size, variables, solution)
		for i in range(size):
			self.row_labels=[]
			for j in range(size):
				self.row_labels.append(Button(self.row[3], textvariable=variables[i][j], height=2, width=3, relief=SUNKEN, state=DISABLED))
				self.row_labels[j].grid(row=i, column=j)

			self.board_labels.append(self.row_labels)

		self.row[4].pack(fill=X)

	# the starting window
	def startWindow(self, to_forget=None, to_destroy=None):
		self.clearWidgets(to_forget, to_destroy)

		self.row[0].pack(fill=X)

	# adjusts index_brd and index_sol by increments, with checks to not go out of bounds, and
	# calls another function (or not), depending on mode.
	def updateIndexes(self, a, b, mode, to_forget=None, to_destroy=None):
		if b != None:
			if ((self.index_sol + b) < len(self.board[self.index_brd]['solutions']) and (self.index_sol + b) >= 0):
				self.index_sol = self.index_sol + b
		else:
			self.index_sol = 0

		if ((self.index_brd + a) < len(self.board) and (self.index_brd + a) >= 0):
			self.index_brd = self.index_brd + a

		if mode == 1:
			self.showBoard(self.index_brd, self.index_sol, to_forget=to_forget, to_destroy=to_destroy)
		if mode == 2:
			self.showSolutions(self.index_brd, self.index_sol, to_forget=to_forget, to_destroy=to_destroy)

	# insert translated algo here to get the board state
	# this will only be called ONCE, in showBoard,
	# so it should loop through each puzzle and solve them at once.
	def solveNChancellorsProblem(self):
		for b in self.board:
			# to get the board state:
			print(self.board[b]['board'])

			# to get the solution list:
			print(self.board[b]['solutions'])

			# to create a list of the same size as board:
			size = self.board[b]['size']
			lst = [[0 for j in range(size)] for i in range(size)]
			print(lst)

			# to copy a list (py references only, you need this to create a new one)
			lst2 = [row[:] for row in lst]

			# to assign a value to a cell:
			lst[0][0] = 1
			lst2[size-1][size-1] = 1

			# to add to the solutions:
			self.board[b]['solutions'].append(lst)
			self.board[b]['solutions'].append(lst2)
			self.board[b]['solutions'].append(self.board[b]['board'])

if __name__ == "__main__":
	root=Tk()
	root.title("N-Chancellors Problem")
	app = NChancellorsApp(root)
	root.mainloop()

