from sys import argv
import collections
import string
import json
import random
import pathlib



fpath = pathlib.Path(__file__).parent.absolute() / 'sessions.json'
fpath2 = pathlib.Path(__file__).parent.absolute() / 'sessions2.json'
f = open(fpath,'r')
text_file = open(fpath2, "w")

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

data = json.load(f)

for z in data['_items']:
    if z['userInputs'] == None:
        continue
    for i in z['userInputs']:
        line = i["modifiedAt"]
        if line == None:
            continue
        day = line[5:7]
        month = line[8:11]
        counter = 0
        for l in months:
            counter += 1
            if month == i:
                break
        year = line[12:16]
        line = str(year) + '-' + str(counter) + '-' + str(day) + line[16:25] + ".00+00:00"
        i["modifiedAt"] = line


json.dump(data,text_file, indent=2)