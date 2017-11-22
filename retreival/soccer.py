import http.client
import json

connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X-Auth-Token': 'dc62f3aa33b04eb9854b50d84d216ccd', 'X-Response-Control': 'minified'}

# Competetion
connection.request('GET', '/v1/competitions', None, headers)
response = json.loads(connection.getresponse().read().decode())

# Teams in a league
connection.request('GET', '/v1/competitions/398/teams', None, headers)
response = json.loads(connection.getresponse().read().decode())

print(response)
