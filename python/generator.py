# -*- coding: utf-8 -*-

import json, sys
from functions import songAdd

player_data = json.load(open("pachypw.json"))
output_data = json.load(open("sample.txt"))
output_file = open('outputdata.txt', 'w')

for song in player_data["data"]:
	songAdd(song, output_data)

json.dump(output_data, output_file)