# importing the requests library
import requests
import pprint as pp
from collections import Counter
import geopy.distance
import math as Math
import operator

def main():
	x=[]
	totalTime={}
	weather={}
	cities={'TroyAlAtlantaGA':['Montgomery,Al','Columbus,GA','Union Spring,Al','Dothan,Al'],
'AtlantaGATroyAl':['Montgomery,Al','Columbus,GA','union Spring,Al','Dothan,Al'],
'TroyAlTalahaseaFl':['Dothan,Al','Elba,Al','Jacksonville,Fl','Destin,Fl']
	}
	for i in cities['TroyAlTalahaseaFl']:
		totalTime[i]=reRoute('Troy,Al','Talahasea,Fl',i)
		weather[i]=getWeather(i+"US")

	visited={False,False,False,False}
	weather['Dothan,Al']="Snow"
	totalTime = sorted(totalTime.items(), key=operator.itemgetter(1))
	calculateReward(totalTime,weather,cities,'TroyAlTalahaseaFl',visited,0)
	
	
	


#calculateReward('Montgomery')
#print(totalTime)

def calculateReward(totalTime,weather,cities,TroyAlTalahaseaFl,visited,time):
	i=list(totalTime)[time]
	print(i)
	x=weather[i[0]]
	print(x)
	point=0
	x=x.lower()
	y=x.split(" ")
	if(len(y)>1):
		if(y[1]=="clear" or y[1]=="cloudy" or y[1]=="sunshine" or y[1]=="haze"):
			point=5*float(totalTime[time][1]/totalTime[0][1])
			print(point)
			return point
		elif(y[1]=="snow" or y[1]=="rain"):
			if(y[0]=="severe"):
				calculateReward(totalTime,weather,cities,TroyAlTalahaseaFl,visited,time+1)
				print(point)
		else:
			point=0
	else:
		if(y[0]=="haze" or y[0]=="cloud" or y[0]=="sunshine" or y[0]=="clear"):
			point=5*float(totalTime[time][1]/totalTime[0][1])
			print(point)
			return point
		else:
			calculateReward(totalTime,weather,cities,TroyAlTalahaseaFl,visited,time+1)

	return point







def checkWeather(waypoints):
	x=getWeather(waypoints)
	x=x.lower()
	y=x.split(" ")

	if (y[0]=='clear'):
		return False
	if(y[0]=="mild" or y[0]=="partly" or y[0]=="scattered"):
		if(y[1]=="snow" or y[1]=="ice"):
			return (True)
		else:
			return (False)
	else:
		return True

def reRoute(origin,destination,waypoints):
# api-endpoint
	totalTime=0
	
	URL = "https://maps.googleapis.com/maps/api/directions/json?origin="+origin+"&destination="+destination+"&waypoints="+waypoints+"&key= AIzaSyDuxETGeU6d4F6ZO1DqZwAWWrBRWOaFAcM"
	r = requests.get(url = URL)
# extracting data in json formathhttps://www.instagram.com/ttps://www.instagram.com/
	data = r.json()
	data2=[]
	data3=[]
	
	for i in  data['routes'][0]['legs']: 
		z=i['steps']
		for j in z:
			f=j['duration']['text'].split(" ")
			if(f[1]=='min' or f[1]=='mins'):
				totalTime=int(f[0])+totalTime
			elif(len(f)>3):
				totalTime=int(f[0])*60+int(f[2])+totalTime
			else:
				totalTime+=int(f[0])*60

			x=j['html_instructions'].split("<b>")
			if(len(x)>2):
				y=x[2].split("</b>")
			else:
				y=x[1].split("</b>")
			print(y[0])

	return(totalTime)

def getWeather(city):
	URL="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=033509d696ab190c1fb34897a6329071"
	r=requests.get(url=URL)
	data=r.json()

	return(data['weather'][0]['description'])


def getSpeedLimit():
	URL="https://roads.googleapis.com/speedLimits?path=31.8088, 85.9700|32.3668, 86.3000&key=AIzaSyAlV5CD7BaQd2oCbwV5byxnB9toGiwd20U"
	r=requests.get(url=URL)
	data=r.json()
	pp.pprint(data)

def getCity(lat,lng,radius,x):
	radius=radius*1000
	URL="https://maps.googleapis.com/maps/api/place/radarsearch/json?location="+str(lat)+","+str(lng)+"&radius="+str(radius)+"&type=city&key=AIzaSyDTas7nwlV2AZ2jScz2lh4gvUsWSM8B4Ms"
	r=requests.get(url=URL)
	data=r.json()
	for i in data['results']:
		getGeoCode(i['place_id'],x)


def getGeoCode(palceID,x):
	URL="https://maps.googleapis.com/maps/api/geocode/json?place_id="+palceID+"&key=AIzaSyDTas7nwlV2AZ2jScz2lh4gvUsWSM8B4Ms"
	r=requests.get(url=URL)
	data=r.json()
	for i in range(len(data['results'])):
		x.append(data['results'][i]['formatted_address'])
		print(x)


def getLat(place):
	URL="https://maps.googleapis.com/maps/api/geocode/json?address="+place+"&key=AIzaSyDTas7nwlV2AZ2jScz2lh4gvUsWSM8B4Ms"
	r=requests.get(url=URL)
	data=r.json()
	pp.pprint(data['results'][0]['geometry']['location'])
	return (data['results'][0]['geometry']['location'])
def Distance(coords_1,coords_2):

	return(geopy.distance.vincenty(coords_1, coords_2).km)

"""
def Points():
	origin="TROY,AL,US"
	destination="Atlanta,GA,US"

	#reRoute(origin,destination,"Montgomery,Al,US")
	origin_latlang= getLat(origin)
	destination_latlang=getLat(destination)
	
	difference_lat=destination_latlang['lat']-origin_latlang['lat']
	difference_lng=destination_latlang['lng']-origin_latlang['lng']

	if(difference_lng>0 and difference_lat>0):
		ave_lat=(origin_latlang['lat']+destination_latlang['lat'])/2
		ave_lng=(origin_latlang['lng']+destination_latlang['lng'])/2
		distance1=Distance((origin_latlang['lat'],origin_latlang['lng']),(destination_latlang['lat'],destination_latlang['lng']))

		r=Math.floor(distance1/37)
		print(r)
		print(origin_latlang['lat'])
		getCity(origin_latlang['lat']+0.5*r,origin_latlang['lng']+0.5*r,36,x)

	#print(x)
"""
main()