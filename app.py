from flask import Flask
from flask import request
import requests
import math
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
def home():
	return 'Home'


@app.route('/weather')
def weather():
	data = []
	map = {'ishower': 'Rainy', 'mcloudy': 'Partly Cloudy', 'lightrain': 'Light Rain', 'clear': 'Clear', 'pcloudy': 'Partly Cloudy', 'cloudy': 'Cloudy', 'rain': 'Rain', 'snow': 'Snow', 'ts': 'Thunderstorm', 'tsrain': 'Thunderstorm with rain'}
	url = "https://www.7timer.info/bin/api.pl"

	querystring = {"lon": request.args.get('lon'), "lat": request.args.get('lat'), "product": "civillight", "output": "json"}
	response = requests.request("GET", url, params=querystring)
	data_7_days = response.json()["dataseries"]

	for day in data_7_days:
		weather = map[day['weather']]
		max_temp = day['temp2m']['max']
		min_temp = day['temp2m']['min']
		data.append((day['date'], weather, max_temp, min_temp))

	return {'data': data}


@app.route('/ice-cover')
@cross_origin(supports_credentials=True)
def ice_cover():
	r = requests.get("https://global-warming.org/api/arctic-api")
	x = r.json()["result"]
	ice = {}

	for di in x:
		ice[di['year']] = (di['extent'], di['area'])
	
	return {'data' : ice}


@app.route('/air-quality/get-countries')
def air_quality_get_countries():
	url = "http://api.airvisual.com/v2/countries"

	querystring = {"key": "3ca626fb-602b-438d-a4dd-f0049419a3c6"}

	response = requests.request("GET", url, params=querystring)
	data = response.json()["data"]
	print(data)
	countries = [x['country'] for x in data]

	return {'countries': countries}



@app.route('/air-quality/get-states')
def air_quality_get_states():

	url = "http://api.airvisual.com/v2/states"

	country = request.args.get('country')
	querystring = {"country": country, "key": "3ca626fb-602b-438d-a4dd-f0049419a3c6"}

	response = requests.request("GET", url, params=querystring)
	data = response.json()["data"]
	states = [x['state'] for x in data]
	
	return {'states': states}



@app.route('/air-quality/get-aqi')
def air_quality_by_city():
	url = "http://api.airvisual.com/v2/cities"

	aqi = {}
	lst = []

	state = request.args.get('state')
	country = request.args.get('country')
	querystring = {"state": state, 'country': country, "key": "3ca626fb-602b-438d-a4dd-f0049419a3c6"}

	response = requests.request("GET", url, params=querystring)
	data = response.json()["data"]
	cities = [x['city'] for x in data]

	count = 0
	print(cities[0])
	for city in cities:
		url1 = f"https://api.waqi.info/feed/{city}/?token=c90260ee6a7c59629518640c6cbd6fa254f030a5"
		# querystring1 = {"city:": cities[0], "state": state, "country": country, "key": "3ca626fb-602b-438d-a4dd-f0049419a3c6"}

		response = requests.request("GET", url1)
		data = response.json()['data']
		if type(data) is dict:
			aqi[city] = data['aqi']

	#if count > 5: break

	return aqi


@app.route('/methane')
def methane():
	url = 'https://global-warming.org/api/methane-api'
	res = {}
	lst = []

	response = requests.request("GET", url)
	data = response.json()["methane"]

	prev_year = 1983.0
	for x in data:
		_, new_year = math.modf(float(x['date']))
		
		if new_year == prev_year:
			lst.append(float(x['average']))

		else:
			res[prev_year] = round(sum(lst) / len(lst), 2)
			lst = []
			prev_year = new_year

	return {'data': res}


if __name__ == '__main__':
	app.run(debug=True)
