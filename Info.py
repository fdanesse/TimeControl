#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import time
from collections import OrderedDict

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject

from Global import getFechas
# from Tree import Tree


class TreeSemana(Gtk.TreeView):

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.TreeStore(GObject.TYPE_STRING,
            GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING))
        self.set_size_request(100, 150)
        self.set_rules_hint(True)
        self.set_property("enable-tree-lines", True)
        self.set_headers_visible(True)
        self.__set_columnas(['Fecha', 'Entrada', 'Salida', 'Saldo'])
        self.show_all()

    def __set_columnas(self, cols):
        for col in cols:
            index = cols.index(col)
            cellrender = Gtk.CellRendererText()        
            columna = Gtk.TreeViewColumn(col, cellrender, text=cols.index(col))
            columna.set_property('visible', True)
            columna.set_property('resizable', False)
            self.append_column(columna)
            cellrender.set_property("editable", False)


class Info(Gtk.Box):

    def __init__(self):

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, homogeneous=False)

        self.set_border_width(2)

        self.label = Gtk.Label("Selecciona un Funcionario para ver sus datos.")
        self.frame = Gtk.Frame()
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.frame)
        self.frame.set_label(" Semanas: ")
        self.saldo = Gtk.Label('Saldo Mensual: 00:00')
        self.pack_start(self.label, False, False, 0)
        self.pack_start(scroll, True, True, 0)
        self.pack_start(self.saldo, False, False, 5)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        self.frame.add(self.vbox)
        self.show_all()
        
        self.fechas = [] # self._dict = OrderedDict() # semana: {fecha: data}
        self._dict = OrderedDict()
        self._dict_tree = OrderedDict()

    def switch_page_and_set_user(self, user, indice, _dict):
        self.label.set_text('Datos de: %s' % user)
        self._dict = _dict
        keys = self._dict.keys() # meses
        keymes = keys[indice] # mes seleccionado fecha: [entrada, salida, saldo]
        fechas = self._dict[keymes].keys() # fechas de este mes
        # FIXME: hay un error con ultimasemana para el mes de diciembre
        primersemana = datetime.datetime.strptime(fechas[0], '%d/%m/%Y').isocalendar()[1]
        ultimasemana = datetime.datetime.strptime(fechas[-1], '%d/%m/%Y').isocalendar()[1]
        # Todas las fechas de las semanas afectadas
        self.fechas = getFechas(primersemana, ultimasemana)
        self.__repack()
        self.update(self._dict) # para que calcule los saldos

    def __repack(self):
        # Quitar treestores
        children = self.vbox.get_children()
        for child in children:
            self.vbox.remove(child)
            child.destroy()
        
        # Crear treestores para cada semana
        self._dict_tree = OrderedDict()
        for fecha in self.fechas:
            semana = fecha.isocalendar()[1]
            if not semana in self._dict_tree.keys():
                tree = TreeSemana()
                label = Gtk.Label('Saldo Semanal: 00:00')
                self.vbox.pack_start(tree, True, True, 5)
                self.vbox.pack_start(label, False, False, 5)
                self._dict_tree[semana] = (tree, label)

            # las fechas de esta semana se agrega a este treestore
            mes = str(fecha.month)
            strfecha = str(datetime.date.strftime(fecha , '%d/%m/%Y'))
            data = self._dict[mes][strfecha]
            self._dict_tree[semana][0].get_model().append(None, [strfecha, data[0], data[1], data[2]])

    def update(self, _dict):
        self._dict = _dict
        saldomensual = datetime.timedelta(hours=0, minutes=0)
        # recorrer trees
        semanas = self._dict_tree.keys()
        for semana in semanas:
            tree = self._dict_tree[semana][0]
            # actualizar datos
            model = tree.get_model()
            item = model.get_iter_first()
            _iter = None
            suma = datetime.timedelta(hours=0, minutes=0)
            while item:
                _iter = item               
                # obtener fecha del tree
                f = model.get_value(_iter, 0)
                # convertir fecha en datetime.date
                fecha = datetime.datetime.strptime(f , '%d/%m/%Y')
                # tomar el mes de esa fecha
                mes = fecha.month
                # los datos en esta linea del tree se toman de _dict[mes][fecha]
                data = self._dict[str(mes)][f]
                model.set_value(_iter, 1, data[0])
                model.set_value(_iter, 2, data[1])
                model.set_value(_iter, 3, data[2])
                # Calcular el saldo de la semana
                temp = time.strptime(data[2], '%H:%M')
                suma += datetime.timedelta(hours=temp.tm_hour, minutes=temp.tm_min)
                item = model.iter_next(item)
            self._dict_tree[semana][1].set_text('Total Semanal: %s' % suma)
            saldomensual += suma
        # Calcular el saldo del mes
        self.saldo.set_text('Saldo Mensual: %s' % saldomensual)