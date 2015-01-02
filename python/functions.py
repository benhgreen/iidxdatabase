# -*- coding: utf-8 -*-	

import sys, json, httplib, urllib, logging, importio, latch
from security import *

reload(sys)
sys.setdefaultencoding("utf-8")

#strips stupid characters out of song title
def strip(title):
	mod = title.replace('"', '')
	return "".join(char for char in mod if char not in " ()[]-#*†♥♥☆,!öÜ！Λ*？・?#.…、ø~～～〜øＸ↑↓'")

#looks up song title and confirms that it exists in the database
def lookup(title, output):
	if "Wonder Girl" in title:
		title = title.replace("Asada", "Asaba")

	if title == "Vermilion":
		title = "Vermillion"

	stripped_title = strip(title)

	for song in output:
		check = strip(song["name"])
		if stripped_title.lower() == check.lower():
			# print("Matched %s with %s" % (title, check))
			return song
	return "NOTFOUND"

#returns integer corresponding with clear status
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

#adds clear status to output database
def addClears(song_data, output_song):
	if "spa" in song_data:
		output_song["stat_sa"] = clearInt(song_data["spa"])
	if "sph" in song_data:
		output_song["stat_sh"] = clearInt(song_data["sph"])
	if "spn" in song_data:
		output_song["stat_sn"] = clearInt(song_data["spn"])

#attempts to add song to output database
def songAdd(song_data, output):
	output_song = lookup(song_data["song_title"], output)
	if output_song == "NOTFOUND":
		print("Song '%s' was not found!\n" % song_data["song_title"])
		return
	else:
		addClears(song_data, output_song)

scores = []

#gets users clear list
	client = clientGen()
	client.connect()
	queryLatch = latch.latch(1)
	
	def callback(query, message):
		global scores
		
		if message["type"] == "DISCONNECT":
			print "Query in progress when library disconnected"
		if message["type"] == "MESSAGE":
			if "errorType" in message["data"]:
				print "Got an error!" 
			else:
				print "Got data!"
				scores.extend(message["data"]["results"])
		
		if query.finished(): 
			queryLatch.countdown()

	client.query({
		"connectorGuids":[
			"665cb61b-45ed-438c-a31d-a21bb262c028"
		],
		"input": {
			"webpage/url": "https://programmedworld.net/iidx/22/players/%s/records" % userid
		},
		"additionalInput": {
			"665cb61b-45ed-438c-a31d-a21bb262c028": {
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
	
	return scores
