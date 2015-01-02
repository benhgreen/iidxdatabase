# -*- coding: utf-8 -*-

import json, sys
from functions import songAdd, getdatabase

#hardcoded userid
userid = "7605-7298"

#get player database
player_data = getdatabase(userid)
#get template database
output_data = json.load(open("../various databases/sample.txt"))
#prep output file object
output_file = open('outputdata.txt', 'w')

#parse player database and add each clear to output database
for song in player_data:
	songAdd(song, output_data)

json.dump(output_data, output_file)