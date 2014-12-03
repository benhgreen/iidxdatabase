import json, sys
from pprint import pprint

reload(sys)
sys.setdefaultencoding("utf8")

json_data = open('pachypw.json')
output = open('output2.txt', 'w')
data = json.load(json_data)

for song in data["data"]:

	output.write("%s\n" % song["song_title"][0])
