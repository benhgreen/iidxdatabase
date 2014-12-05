# -*- coding: utf-8 -*-

import json, sys
from functions import songAdd, getdatabase

userid = "7605-7298"

player_data = getdatabase(userid)
output_data = json.load(open("../various databases/sample.txt"))
output_file = open('outputdata.txt', 'w')

for song in player_data:
	songAdd(song, output_data)

json.dump(output_data, output_file)