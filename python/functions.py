# -*- coding: utf-8 -*-	

import sys, json, httplib, urllib, logging, importio, latch
from security import *

reload(sys)
sys.setdefaultencoding("utf-8")

def strip(title):
	mod = title.replace('"', '')
	return "".join(char for char in mod if char not in " ()[]-#*†♥♥☆,!öÜ！Λ*？・?#.…、ø~～～〜øＸ↑↓'")

def lookup(title, output):

	if "Wonder Girl" in title:
		title.replace("Asada", "Asaba")

	if title == "Vermilion":
		title = "Vermillion"

	stripped_title = strip(title)

	for song in output:
		check = strip(song["name"])
		if stripped_title.lower() == check.lower():
			# print("Matched %s with %s" % (title, check))
			return song
	return "NOTFOUND"

def clearInt(clear):
	return {
		"No Play": 0,
		"Failed": 1,
		"Assist Clear": 2,
		"Easy Clear": 3,
		"Clear": 4,
		"Hard Clear": 5,
		"Ex Hard Clear": 6,
		"Full Combo": 7
	}.get(clear, "ERROR")

def addClears(song_data, output_song):
	if "spa" in song_data:
		output_song["stat_sa"] = clearInt(song_data["spa"][0])
	if "sph" in song_data:
		output_song["stat_sh"] = clearInt(song_data["sph"][0])
	if "spn" in song_data:
		output_song["stat_sn"] = clearInt(song_data["spn"][0])

def songAdd(song_data, output):
	output_song = lookup(song_data["song_title"][0], output)
	if output_song == "NOTFOUND":
		print("Song '%s' was not found!\n" % song_data["song_title"][0])
		return
	else:
		addClears(song_data, output_song)

def callback(query, message):
	if message["type"] == "DISCONNECT":
    	print "Query in progress when library disconnected"
    	print json.dumps(message["data"], indent = 4)

	if message["type"] == "MESSAGE":
		if "errorType" in message["data"]:
      		print "Got an error!" 
     	 	print json.dumps(message["data"], indent = 4)
    else:
     	 print "Got data!"
     	 print json.dumps(message["data"], indent = 4)
  	if query.finished(): 
  		queryLatch.countdown()

def getdatabase(userid):
	client = clientGen()
	queryLatch = latch(1)

	client.query({
  		"extractorGuids":[
   			"665cb61b-45ed-438c-a31d-a21bb262c028"
  		],
  		"input": {
        	"webpage/url": "https://programmedworld.net/iidx/22/players/9903-3601/records"
   		},
    	"additionalInput": {
        	"665cb61b-45ed-438c-a31d-a21bb262c028": {
	            "cookies": [],
	            "domainCredentials": {
	                "programmedworld.net": {
	                    "username": getPWuser(),
	                    "password": getPWpwd(),
	                }
	            }
	        }
	    }
	}, callback)

	queryLatch.await()

	client.disconnect()
	pass