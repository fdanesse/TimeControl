#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import datetime
from collections import OrderedDict

HOME = os.environ["HOME"]
# BASE_PATH = os.path.dirname(__file__)


PERSISTENCIA = os.path.join(HOME, "TimeControlData")
if not os.path.exists(PERSISTENCIA):
    os.mkdir(PERSISTENCIA)


'''
def __filter_fechas(fecha, mes):
    # quita sabados y domingos
    return (fecha.month == mes) and (fecha.weekday() < 5)
'''

'''
def __filter_fechas2(fecha, primersemana, ultimasemana):
    # fechas entre nºs de semana
    return (fecha.isocalendar()[1] in range(primersemana, ultimasemana+1))
'''

'''
def getFechas(primersemana, ultimasemana):
    anio = 2018
    meses = range(3, 13)
    cal = calendar.Calendar()
    fechas = []
    for mes in meses:
        f = [item for item in cal.itermonthdates(
            anio, mes) if __filter_fechas(item, mes)]
        fechas.extend(f)
    fechas = [item for item in fechas if __filter_fechas2(
        item, primersemana, ultimasemana)]
    return fechas
'''

'''
def __getDatesModel():
    anio = 2018
    meses = range(3, 13)
    cal = calendar.Calendar()
    _dict = OrderedDict()
    for mes in meses:
        _dict[mes] = OrderedDict()
        fmes = cal.itermonthdates(anio, mes)
        fechas = [str(datetime.date.strftime(item , '%d/%m/%Y')) \
            for item in fmes if __filter_fechas(item, mes)]
        for fecha in fechas:
            _dict[mes][fecha] = ['00:00', '00:00', '00:00']
    return _dict
'''


def __filterSemana(fecha, semana):
    return (datetime.datetime.strptime(
        fecha, '%d/%m/%Y').isocalendar()[1] == semana)


def getDataSemana(user, semana, data):
    fechas = [item for item in data.get(
        'horas', {}).keys() if __filterSemana(item, semana)]
    _dict = OrderedDict()
    fs = []
    for fecha in fechas:
        fs.append(datetime.datetime.strptime(fecha, '%d/%m/%Y'))
    fs.sort()
    for fecha in fs:
        key = str(datetime.date.strftime(fecha, '%d/%m/%Y'))
        _dict[key] = data['horas'][key]
    return _dict


def adduser(num, name):
    path = os.path.join(PERSISTENCIA, num)
    if os.path.exists(path):
        return False
    archivo = open(path, "w")
    _dict = {'nombre': name, 'horas': {}}  #__getDatesModel()
    archivo.write(json.dumps(
        _dict,
        indent=4,
        separators=(", ", ":"),
        sort_keys=True))
    archivo.close()
    return True


'''
def getUsers():
    archs = os.listdir(PERSISTENCIA)
    for arch in archs:
        archs[archs.index(arch)] = arch.split('.')[0]
    archs.sort()
    return archs
'''

'''
def getDataUser(funcionario):
    archivo = open(os.path.join(PERSISTENCIA, funcionario + '.json'), "r")
    _dict = json.load(archivo, "utf-8")
    archivo.close()
    ret = OrderedDict()

    # Ordenar meses en OrderedDict
    meses = _dict.keys()
    l = []
    for mes in meses:
        l.append(int(mes))
    l.sort()

    # Ordenar fechas en OrderedDict
    for a in l: # lista de string que representa los meses
        ret[str(a)] = OrderedDict()
        fechas = _dict[str(a)].keys() # lista de fechas en string

        lista = [] # lista de fechas en datetime
        for f in fechas:
            lista.append(datetime.datetime.strptime(f , '%d/%m/%Y'))
        lista.sort()

        for i in lista:
            fecha = datetime.date.strftime(i , '%d/%m/%Y')
            ret[str(a)][fecha] = _dict[str(a)][fecha]

    return ret
'''


def getDataUser(num):
    path = os.path.join(PERSISTENCIA, num)
    _dict = {}
    if os.path.exists(path):
        arch = open(path, "r")
        _dict = json.load(arch, "utf-8")
        arch.close()
    return _dict


def addData(num, _new):
    _dict = getDataUser(num)
    if _dict:
        _dict['horas'][_new.keys()[0]] = _new[_new.keys()[0]]
        path = os.path.join(PERSISTENCIA, num)
        archivo = open(path, "w")
        archivo.write(json.dumps(
            _dict,
            indent=4,
            separators=(", ", ":"),
            sort_keys=True))
        archivo.close()
        return True
    else:
        return False


def validateTime(_new):
    try:
        temp = time.strptime(_new, '%H:%M')
        return time.strftime('%H:%M', temp)
    except:
        return False


def getDiferenciaHorasMinutos(inicio, final):
    # Recibe y devuelve datos en string listos para gardar y mostrar.
    # string a tiempo
    temp = time.strptime(inicio, '%H:%M')
    t1 = datetime.timedelta(hours=temp.tm_hour, minutes=temp.tm_min)
    temp = time.strptime(final, '%H:%M')
    t2 = datetime.timedelta(hours=temp.tm_hour, minutes=temp.tm_min)
    temp = time.strptime('00:00:00', '%H:%M:%S')
    if t2 > t1:
        # diferencia timedelta
        # FIXME: Resultado negativo en este calculo agrega -1 day
        # lo que provoca un error en el formato %H:%M
        dif = str(t2 - t1)
        # string a time
        temp = time.strptime(dif, '%H:%M:%S')
        # time a string despreciando los segundos
    return time.strftime('%H:%M', temp)


def getTotalHoras(values):
    temp = time.strptime('00:00', '%H:%M')
    dif = datetime.timedelta(hours=temp.tm_hour, minutes=temp.tm_min)
    for val in values:
        temp = time.strptime(val[0], '%H:%M')
        t1 = datetime.timedelta(hours=temp.tm_hour, minutes=temp.tm_min)
        temp = time.strptime(val[1], '%H:%M')
        t2 = datetime.timedelta(hours=temp.tm_hour, minutes=temp.tm_min)
        if t2 > t1:
            dif += t2 - t1
    temp = time.strptime(str(dif), '%H:%M:%S')
    return time.strftime('%H:%M', temp)


'''
def updateUser(user, _dict):
    path = os.path.join(PERSISTENCIA, user + '.json')
    archivo = open(path, "w")
    archivo.write(json.dumps(
        _dict,
        indent=4,
        separators=(", ", ":"),
        sort_keys=True))
    archivo.close()
'''
