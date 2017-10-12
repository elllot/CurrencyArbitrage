from math import log, exp
from collections import defaultdict
from decimal import getcontext, Decimal
from CurrencyDigraph import CurrencyDigraph

class AribitrageFinder:

	def __init__(self, starting_amount):
		self.starting_amount = starting_amount
		self.digraph = CurrencyDigraph()
		self.src = self.select_starting_currency()
		self.digraph.set_source(self.src)
		self.find_arbitrage()

	def select_starting_currency(self):
		"""
		Method for handling user input in selecting a starting currency

		:returns: int
		"""
		print(chr(27) + "[2J") # clear screen
		self.digraph.print_currency_list()
		var = input('Select a currency (pick an ID): ')
		while not var.isdigit() or int(var) not in self.digraph.scraper.keys:
			print('Please select a valid ID...')
			var = input('Select a currency (pick an ID): ')
		src = int(var)
		print('You picked {0}'.format(self.digraph.scraper.keys[src]))
		return src

	def arbitrage_profit(self):
		"""
		A helper method for printing the arbitrage cycle. Shows how much can 
		be made relative to the starting amount. Prints details of arbitrage
		opportunity.
		
		:param amount: starting amount
		:param cycle: found cycle
		:param W: weights hashmap
		:param keys: hashmap of keys from ID to currency code
		:returns: void
		"""
		#print("negative cycle:", cycle)
		cycle = self.digraph.find_cycle(self.src)
		orig = result_amount = self.starting_amount
		trade_sequence = []
		for i in range(len(cycle)):
			trade_sequence.append(self.digraph.scraper.keys[cycle[i]])
			result_amount *= exp(-self.digraph.weights[(cycle[i], cycle[(i+1)%len(cycle)])])
			#_sum += W[(neg_cycle[i], neg_cycle[(i+1)%len(neg_cycle)])]
		profit_percent = round((result_amount - orig) / float(orig), 5)
		print('->'.join(trade_sequence))
		print("started with: {0} | Ended With: {1} | {2}% profit []|:^)".format(orig, result_amount, profit_percent))

	def find_arbitrage(self):
		"""
		Bellman-Ford algorithm to detect negative weight cycles.
		
		:param src: starting currency
		:param starting_amount: starting amount in currency
		:returns: void
		"""
		#digraph = CurrencyDigraph(self.src)
		# Bellman-Ford
		for i in range(len(self.digraph.graph)-1):
			for w in self.digraph.weights:
				# w is a tuple in the form of (u, v)
				u, v = w
				if self.digraph.distances[u] != float("inf"):
					temp = self.digraph.distances[u] + self.digraph.weights[w] # distance(u) + weight(u, v)
					if temp < self.digraph.distances[v]: # if shorter path found
						self.digraph.distances[v] = temp
						self.digraph.parents[v] = u
						if v == self.src: # negative path back to source found. Terminate
							self.arbitrage_profit()
							return
		# negative cycle detection
		for w in self.digraph.weights:
			u, v = w
			temp = self.digraph.distances[u] + self.digraph.weights[w]
			if v == self.src: # limit to only cycles including src currency
				if temp < self.digraph.distances[v]:
					self.arbitrage_profit()
					return
		# no arbitrage found
		print("no Arbitrage")
	
if __name__ == '__main__':
	# example usage
	#arbitrage(1, 1000)
	a = AribitrageFinder(1000)