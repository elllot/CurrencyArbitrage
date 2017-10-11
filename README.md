# CurrencyArbitrage
Beautiful Soup &amp; Selenium for webscraping. Bellman Ford negative weight detection for finding arbitrage cycles. Wanted to implement this as it seemed like a very interesting problem.

Currently only supports detection of any Arbitrage opportunity. Could possibly augment the process by only detecting cycles with the starting currency in.

Algorithm implemented two ways:

	1. iterate V-1 times over entire graph as speicified in Bellman-Ford's algorithm

	2. check for every V iterations of the call to see if there's a cycle. This could be 
	   more efficient as we're only looking for a single cycle, which could be found after
	   each G iteration

Uses FX data from x-rates.com
