from bs4 import BeautifulSoup
import urllib3
import requests

def try_generate_key(keys, strs, key, cStr):
	if cStr not in strs:
		strs[cStr] = key
		keys[key] = cStr
		return key + 1
	return key

def scrape():
	url = "http://www.x-rates.com"
	http = urllib3.PoolManager()
	request_main = http.request('GET', url)
	soup_main = BeautifulSoup(request_main.data, "lxml")
	target = soup_main.find("ul", class_="currencyList ratestable")

	rates, strs, keys = {}, {}, {}

	key = 0
	for a in target.find_all("a"):
		# add the current base key if it isn't in the currencies mapping
		key = try_generate_key(keys, strs, key, a.text)

		page_url = a['href'] + "&amount=1"
		request = http.request('GET', page_url)
		soup = BeautifulSoup(request.data, "lxml")
		table = soup.find_all("table")

		for t in table:
			t_body = t.find("tbody")
			rows = t_body.find_all("tr")
			for r in rows:
				c = r.find_all("td")
				c = [item.text.strip() for item in c]
				# add currency if it isn't in the key hashmap
				key = try_generate_key(keys, strs, key, c[0])

				forward = (strs[a.text], strs[c[0]])
				if forward not in rates: 
						rates[forward] = float(c[1])
						# adding reverse to save duplicated work
						rates[(forward[1], forward[0])] = float(c[2])

	return rates, strs, keys