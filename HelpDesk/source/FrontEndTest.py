import requests
Link = 'http://192.168.29.80:5000'
query = "L&T Technology services"
Outs = requests.get(Link+'/'+str(query))
Title , FileOutput = Outs.json()

print("Title  :" , Title)