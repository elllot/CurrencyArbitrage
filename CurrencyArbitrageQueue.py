from math import log, exp
from collections import defaultdict, deque
from decimal import getcontext, Decimal
from Scrape import scrape

# See if I can implement string matching to parse user input to recommend 
# correct input

"""
#	Method for Generating a graph from scraped data
#
"""
def generate_graph():
	rates, strs, keys = scrape()
	graph, weights = defaultdict(set), {}
	for r in rates: 
		graph[r[0]].add(r[1])
		# using negative log to transform the problem into adding weights 
		weights[r] = -log(rates[r]) 
	return graph, weights, strs, keys

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

# Bellman-Ford algorithm to detect negative weight cycles
def arbitrage(src):
	G, W, strs, keys = generate_graph()
	
	D = {i: float("inf") for i in G}
	D[src] = 0.0
	parents = {}
	# Bellman-Ford Queue
	queue = deque([src])
	queued = set([src])	
	calls = 0
	while queue:
		v = queue.popleft()
		queued.remove(v)
		calls, cycle = relax(v, D, W, G, parents, queue, queued, calls)
		if cycle: 
			arbitrage_profit(1000, cycle, W, keys)
	return None, None

def find_cycle(v, parents):
	print("looking starting at", v)
	V, res = set(), []
	while v not in V:
		V.add(v)
		res.append(v)
		v = parents[v]
	print("cycle start:", v)
	print("cycle:", res[res.index(v):])
	return res[res.index(v):][::-1]

def cyclefind(v, parents, W, R, B):
	if v in B: return
	if v in R: return find_cycle(v, parents)
	R.add(v)
	if v in parents:
		#for vt in parents[v]:
		cycle = cyclefind(parents[v], parents, W, R, B)
		if cycle: return cycle
	R.remove(v); B.add(v)

# using top sort for detecting cycles
def negativeCycle(parents):
	W, R, B = set(), set(), set()
	for k,v in parents.items():
		W.add(k); W.add(v)
	for v in W:
		res = cyclefind(v, parents, W, R, B) 
		if res: return res

def relax(v, D, W, G, parents, queue, queued, calls):
	print(G[v], D)
	for vt in G[v]:
		weight = W[(v, vt)]
		_d = D[v] + weight
		if _d < D[vt]: # update distance
			#print("relaxing vertex", vt, "from", D[vt], "to", _d)
			D[vt] = _d
			parents[vt] = v
			if vt not in queued:
				queued.add(vt)
				queue.append(vt)
		if calls % len(G) == 0:
			res = negativeCycle(parents)
			if res: return calls, res
		calls += 1
	return calls, None 

if __name__ == '__main__':
	# example usage
	arbitrage(1)
