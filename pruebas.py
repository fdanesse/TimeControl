
import sys
import calendar
import time
import datetime
from collections import OrderedDict

_dict = {
    "3":{
        "01/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "02/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "05/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "06/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "07/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "08/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "09/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "12/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "13/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "14/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "15/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "16/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "19/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "20/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "21/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "22/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "23/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "26/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "27/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "28/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "29/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ], 
        "30/03/2018":[
            "00:00", 
            "00:00", 
            "00:00"
        ]
    }}

# https://stackoverflow.com/questions/2600775/how-to-get-week-number-in-python
saldo = 0
fechas = []
for f in _dict['3'].keys():
    fechas.append(datetime.datetime.strptime(f , '%d/%m/%Y'))
fechas.sort()

_dictFechas = OrderedDict()
for fecha in fechas:
    # fecha.strftime("%V")
    week = fecha.isocalendar()[1] # year, weeknumber and weekday
    if not week in _dictFechas.keys():
        _dictFechas[week] = []
    _dictFechas[week].append(fecha)

for key in _dictFechas.keys():
    print key, _dictFechas[key]