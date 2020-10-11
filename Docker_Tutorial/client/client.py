import urllib.request

fp = urllib.request.urlopen("http://localhost:5000")

content = fp.read().decode("utf-8")

print(content)

fp.close()