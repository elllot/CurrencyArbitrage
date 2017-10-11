from math import log, exp
from collections import defaultdict
from decimal import getcontext, Decimal
from Scrape import scrape

"""
#	Method for Generating a graph from scraped data
#
"""
def generate_graph():
	# process and obtain relevant information 
	rates, strs, keys = scrape()
	graph, weights = defaultdict(list), {}
	# generating an adjacency list and a hashmap of edges that stores
	# hashed (u, v) tuples as keys and their respective weights as values
	for r in rates: 
		graph[r[0]].append(r[1]) 
		# using negative log to transform the problem into adding weights 
		weights[r] = -log(rates[r]) 
	return graph, weights, strs, keys

"""
#	Method for finding cycles in the parent map. 
#
"""
def find_cycle(v, parents):
	V, res = set(), []
	while v not in V:
		V.add(v)
		res.append(v)
		v = parents[v]
	return res[res.index(v):][::-1]

"""
#	A helper method for printing the arbitrage cycle. Shows how much can 
#	be made relative to the starting amount.
#
"""
def arbitrage_profit(amount, cycle, W, keys):
	print("negative cycle:", cycle)
	orig = amount
	trade_sequence = []
	for i in range(len(cycle)):
		trade_sequence.append(keys[cycle[i]])
		amount *= exp(-W[(cycle[i], cycle[(i+1)%len(cycle)])])
		#_sum += W[(neg_cycle[i], neg_cycle[(i+1)%len(neg_cycle)])]
	print('->'.join(trade_sequence))
	print("started with:", orig, "| Ended With: ", amount)

"""
#	Bellman-Ford algorithm to detect negative weight cycles
#
"""
def arbitrage(src, starting_amount):
	G, W, strs, keys = generate_graph()
	#print(strs)
	# initializing distances to infinity
	D = {i: float("inf") for i in G}
	D[src] = 0.0 # distance to start
	# parent map to backtrack later for finding cycles
	parents = {}
	# Bellman-Ford
	for i in range(len(G)-1):
		for w in W:
			# w is a tuple in the form of (u, v)
			u, v = w
			if D[u] != float("inf"):
				temp = D[u] + W[w] # distance(u) + weight(u, v)
				if temp < D[v]: # if shorter path found
					D[v] = temp
					parents[v] = u
					if v == src: # negative path back to source found. Terminate
						arbitrage_profit(starting_amount, find_cycle(v, parents), W, keys)
						return
	# negative cycle detection
	for w in W:
		u, v = w
		temp = D[u] + W[w]
		if v == src: # limit to only cycles including src currency
			if temp < D[v]:
				arbitrage_profit(starting_amount, find_cycle(v, parents), W, keys)
				return
	print("no Arbitrage")
	
if __name__ == '__main__':
	# example usage
	arbitrage(1, 1000)