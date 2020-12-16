import random as rand
import numpy as np

class Game:
	def __init__(self, code = None, colors=6, pegs=4, total_guesses=10, silent=False):
		if not silent:
			print("Starting new game with", colors, "colors,", pegs," pegs, and ", total_guesses, "total guesses allowed")
		if code == None:
			self.answer = []
			for i in range(pegs):
				self.answer.append(rand.randrange(colors))
		else:
			assert len(code) == pegs, "Code incorrect length!"
			self.answer = code

		self.board = []
		self.guesses = []
		self.solved = False
		self.failed = False
		self.silent = silent
		self.pegs = pegs
		self.colors = colors

		self.total_guesses = total_guesses

	def guess(self, *guesses):
		if self.solved:
			print("Already solved!")
			return
		elif self.failed:
			print("Sorry, you lost :(")
			return
		assert self.pegs == len(guesses)
		total_guesses = self.total_guesses
		xs = 0
		os = 0

		leftover_c = []
		leftover_g = []
		for i in range(self.pegs):
			if self.answer[i] == guesses[i]:
				os = os+1
			else:
				leftover_c.append(self.answer[i])
				leftover_g.append(guesses[i])
		for g in leftover_g:
			exists = False
			for c in leftover_c:
				if g == c:
					exists = True
			if exists:
				xs = xs+1
				leftover_c.remove(c)

		assert xs+os < (self.pegs+1), "What happened??"
		roundguess = []
		for i in range(os):
			roundguess.append("o")
		for i in range(xs):
			roundguess.append("x")
		for i in range(self.pegs-os-xs):
			roundguess.append("_")
		self.guesses.append(guesses)
		self.board.append(roundguess)

		if not self.silent:
			self.display_board()

		win = True
		for i in roundguess:
			if i != "o":
				win = False
		if win:
			if not self.silent:
				print("Congrats you win!")
			self.solved = True
		elif len(self.guesses) == self.total_guesses:
			if not self.silent:
				print("Game over, the correct answer was ", self.answer)
			self.failed = True

		return os, xs

	def rounds(self):
		return len(self.guesses)

	def cheat(self):
		return self.answer

	def display_board(self):
		print("Board:")
		for i in np.arange(self.total_guesses):
			if i <= (len(self.board)-1):
				start = "|"
				for z in range(self.pegs):
					start = start + " " + str(self.guesses[i][z])
				start = start + " |"
				for z in range(self.pegs):
					start = start + " " + str(self.board[i][z])
				start = start + " |"
				print(start)
				#print("| ", self.guesses[i][0], " ", self.guesses[i][1], " ", self.guesses[i][2], " ", self.guesses[i][3], " | ",
				#	self.board[i][0], " ", self.board[i][1], " ", self.board[i][2], " ", self.board[i][3], " |")
			else:
				start = "|"
				for z in range(self.pegs):
					start = start + " _ "
				start = start + " |"
				for z in range(self.pegs):
					start = start + " _ "
				start = start + " |"
				print(start)