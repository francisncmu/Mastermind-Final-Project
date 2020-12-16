import numpy as np
import random as rand
import mastermind as m
import xlsxwriter

class Solver:
	def __init__(self, pegs=4, colors=6):
		hypotheses = []
		if pegs == 4:
			for i in range(colors):
				for j in range(colors):
					for k in range(colors):
						for l in range(colors):
							hypotheses.append(([i, j, k, l], 1/(pow(4, colors))))
		elif pegs == 5:
			for i in range(colors):
				for j in range(colors):
					for k in range(colors):
						for l in range(colors):
							for h in range(colors):
								hypotheses.append(([i, j, k, l, h], 1/(pow(5, colors))))
		elif pegs == 6:
			for i in range(colors):
				for j in range(colors):
					for k in range(colors):
						for l in range(colors):
							for h in range(colors):
								for y in range(colors):
									hypotheses.append(([i, j, k, l, h, y], 1/(pow(6, colors))))
		self.pegs = pegs
		self.hypotheses = hypotheses
		self.colors = colors

	def guess(self, game, red=1/4, white=3/16, force=None):
		assert self.pegs == game.pegs, "Different amount of pegs"
		assert self.colors == game.colors, "Different amount of colors"
		max_prob = 0
		max_hypotheses = []
		for h, p in self.hypotheses:
			if max_prob < p:
				max_prob = p
				max_hypotheses = [h]
			elif max_prob == p:
				max_hypotheses.append(h)
		if force == None:
			choice = rand.choice(max_hypotheses) #chooses one of the choices with the highest hypotheses chance
		else:
			choice = force #Forces a specific guess in the form of a list
		os, xs = game.guess(*choice)
		new_hypotheses = []
		for h, chance in self.hypotheses:
			oc = 0
			xc = 0
			leftover_c = []
			leftover_g = []

			if choice == h:
				new_hypotheses = new_hypotheses #filler
			else:
				for i in range(len(choice)):
					if h[i] == choice[i]:
						oc = oc+1
					else:
						leftover_c.append(h[i])
						leftover_g.append(choice[i])

				for g in leftover_g:
					exists = False
					for c in leftover_c:
						if g == c:
							exists = True
					if exists:
						xc = xc+1
						leftover_c.remove(c)
				if oc == os and xs == xc:
					new_hypotheses.append((h, ((oc*red) + (xs*white))))#Red and White are changeable parameters
		self.hypotheses = new_hypotheses

	def reset(self):
		colors = self.colors
		pegs = self.pegs
		hypotheses = []
		if pegs == 4:
			for i in range(colors):
				for j in range(colors):
					for k in range(colors):
						for l in range(colors):
							hypotheses.append(([i, j, k, l], 1/(pow(4, colors))))
		elif pegs == 5:
			for i in range(colors):
				for j in range(colors):
					for k in range(colors):
						for l in range(colors):
							for h in range(colors):
								hypotheses.append(([i, j, k, l, h], 1/(pow(5, colors))))
		elif pegs == 6:
			for i in range(colors):
				for j in range(colors):
					for k in range(colors):
						for l in range(colors):
							for h in range(colors):
								for y in range(colors):
									hypotheses.append(([i, j, k, l, h, y], 1/(pow(6, colors))))
		self.hypotheses = hypotheses

	def solve(self, game, hush=False): #Basic Solving Technique
		self.reset()
		while game.solved == False and game.failed == False:
			self.guess(game)
		if game.solved==True:
			if not hush:	
				print("Solved in", game.rounds(), "turns.")
			return True, game
		else:
			if not hush:
				print("Whoops we lost")
			return False, game

	def solveF(self, game, firstGuess, hush=False): #Basic Solving Technique
		self.reset()
		self.guess(game, force=firstGuess)
		while game.solved == False and game.failed == False:
			self.guess(game)
		if game.solved==True:
			if not hush:	
				print("Solved in", game.rounds(), "turns.")
			return True, game
		else:
			if not hush:
				print("Whoops we lost")
			return False, game

	def multisolve(self, games):
		wins = []
		losses = 0
		codes = []
		most = 0
		least = 10
		for i in range(games):
			g = m.Game(colors = self.colors, pegs=self.pegs, silent=True)
			win, game = self.solve(g, hush=True)
			guesses = game.rounds()
			answer = game.cheat()
			if guesses < least:
				least = guesses
				least_g = answer
			if guesses > most:
				most = guesses
				most_g = answer
			if win:
				wins.append(guesses)
			else:
				game.display_board()
				losses = losses + 1
				codes.append(answer)

		print("Won", len(wins), "number of times with an average of: ", sum(wins)/len(wins), "rounds played.")
		print("The game that took the most guesses was", most, "with the code", most_g)
		print("The game that took the least guesses was", least, "with the code", least_g)
		print("Lost", losses, "number of times to these codes:", codes)
		return codes

	def multisolveF(self, firstGuess, games):
		wins = []
		losses = 0
		codes = []
		most = 0
		least = 10
		for i in range(games):
			g = m.Game(colors = self.colors, pegs=self.pegs, silent=True)
			win, game = self.solveF(g, firstGuess, hush=True)
			guesses = game.rounds()
			answer = game.cheat()
			if guesses < least:
				least = guesses
				least_g = answer
			if guesses > most:
				most = guesses
				most_g = answer
			if win:
				wins.append(guesses)
			else:
				game.display_board()
				losses = losses + 1
				codes.append(answer)

		print("Won", len(wins), "number of times with an average of: ", sum(wins)/len(wins), "rounds played.")
		print("The game that took the most guesses was", most, "with the code", most_g)
		print("The game that took the least guesses was", least, "with the code", least_g)
		print("Lost", losses, "number of times to these codes:", codes)
		return codes

	def multisolveAll(self, iterations): #For testing purposes specifically
		total_results = []
		colors = self.colors
		for i in range(iterations):
			codelist = []
			if self.pegs == 4:
				for i in range(colors):
					for j in range(colors):
						for k in range(colors):
							for l in range(colors):
								codelist.append([i, j, k, l])
			elif self.pegs == 5:
				for i in range(colors):
					for j in range(colors):
						for k in range(colors):
							for l in range(colors):
								for h in range(colors):
									codelist.append([i, j, k, l, h])
			elif self.pegs == 6:
				for i in range(colors):
					for j in range(colors):
						for k in range(colors):
							for l in range(colors):
								for h in range(colors):
									for y in range(colors):
										codelist.append([i, j, k, l, h, y])

			codesResults = []
			for c in codelist:
				g = m.Game(code=c, colors = self.colors, pegs=self.pegs, silent=True)
				win, game = self.solve(g, hush=True)
				codesResults.append(game.rounds())
			total_results.append(codesResults)

		workbook = xlsxwriter.Workbook('Results.xlsx')  #Write to an Excel Doc
		sheet1 = workbook.add_worksheet()
		for i in range(len(codelist)):
			sheet1.write(i+1, 0, str(codelist[i]))

		for i in range(len(total_results)):
			for j in range(len(total_results[i])):
				sheet1.write(j+1, i+1, total_results[i][j])

		total_results2 = []
		for i in range(iterations):
			codesResults = []
			for c in codelist:
				g = m.Game(code=c, colors = self.colors, pegs=self.pegs, silent=True)
				win, game = self.solveF(g, [0, 0, 1, 1], hush=True)#Change this line to test
				codesResults.append(game.rounds())
			total_results.append(codesResults)

		sheet2 = workbook.add_worksheet()
		for i in range(len(codelist)):
			sheet2.write(i+1, 0, str(codelist[i]))

		for i in range(len(total_results2)):
			for j in range(len(total_results2[i])):
				sheet2.write(j+1, i+1, total_results2[i][j])
		workbook.close() 