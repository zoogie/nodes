import os
pyvers=3
try:
	import urllib.request
except:
	import urllib2
	pyvers=2

def download(url, dest):
	try:
		data=b""
		if pyvers==3:
			response = urllib.request.urlopen(url)
		else:
			response = urllib2.urlopen(url)
		html = response.read()
		if os.path.exists(dest):
			with open(dest, "rb") as f:
				data = f.read()
		if len(data) < len(html):
			with open(dest, "wb") as f:
				f.write(html)
				print("Updating " + dest + " success!")
		else:
			print(dest + " is already up-to-date!")
	except:
		print("Error updating " + dest)


download("https://github.com/zoogie/nodes/blob/master/old-v2.dat?raw=true", "old-v2.dat")
download("https://github.com/zoogie/nodes/blob/master/new-v2.dat?raw=true", "new-v2.dat")