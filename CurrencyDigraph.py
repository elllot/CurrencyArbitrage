from Scraper import Scraper
from collections import defaultdict
from math import log

class CurrencyDigraph:

	def __init__(self, src = None):
		self.graph = defaultdict(list)
		self.weights = {}
		# initializes a scraper object to scrape data
		self.scraper = Scraper()
		self.generate_graph()
		self.parents = {}
		self.distances = {vertex: float("inf") for vertex in self.graph}
		if src:
			self.set_source(src)
		self.currency_list = self.currencies_to_list()
		self.print_cache = []
		self.items_per_line = 4

	def set_source(self, src):
		"""
		Helper method for setting starting (source) currency

		:returns: void
		"""
		self.distances[src] = 0.0

	def generate_graph(self):
		"""
		Method for Generating a graph from scraped data
		
		:returns: void
		"""
		# process and obtain relevant information 
		# generating an adjacency list and a hashmap of edges that stores
		# hashed (u, v) tuples as keys and their respective weights as values
		for r in self.scraper.rates: 
			self.graph[r[0]].append(r[1]) 
			# using negative log to transform the problem into adding weights 
			self.weights[r] = -log(self.scraper.rates[r]) 

	def find_cycle(self, v):
		"""
		Method for finding cycles in the parent map. Uses a DFS on the 
		parent map starting from the given vertex v
		
		:param v: vertex in the cycle
		:param parents: the parent map
		:returns: list
		"""
		V, res = set(), []
		while v not in V:
			V.add(v)
			res.append(v)
			v = self.parents[v]
		return res[res.index(v):][::-1]

	def currencies_to_list(self):
		return sorted([[k,v] for k,v in self.scraper.strs.items()],key = lambda x: x[1])

	def print_currency_list(self):
		"""
		Helper method for printing currency list. # of currency items per line depends on the
		items_per_line variable. Caches the previous result so that it can efficiently reprint
		if necessary.

		:returns: void
		"""
		print('Currency List:')
		# if a result is cached: print the cached list instead
		if self.print_cache:
			for line in self.print_cache:
				print(line, '\n')
		else:
			itr = 0
			while itr < len(self.currency_list):
				end = itr + self.items_per_line
				self.print_cache.append(self.currency_list[itr:min(len(self.currency_list),end)])
				print(self.print_cache[-1], '\n')
				itr = end

