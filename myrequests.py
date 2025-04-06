import requests

#Create requests to google
x = requests.get('http://172.19.17.96:5000/access', params = {"id":"1"} )

print(x)