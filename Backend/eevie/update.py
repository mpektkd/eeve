from eevie.models import *
import json

f = open('Data/station_info_gr.json', 'r')
data = json.load(f)

for i in data:
    Station.update(**i)