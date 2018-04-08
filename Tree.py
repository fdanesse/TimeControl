#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject

from Global import getDiferenciaHorasMinutos


class Tree(Gtk.TreeView):

    __gsignals__ = {
        "updateuser": (GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING,
            GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.TreeStore(GObject.TYPE_STRING,
            GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.set_rules_hint(True)
        self.set_property("enable-tree-lines", True)
        self.set_headers_visible(True)
        self.__set_columnas(['Fecha', 'Entrada', 'Salida', 'Saldo'])
        self.show_all()            
        self._mes = 0
        self._dict = {}

    def set_data_mes(self, user, mes, _dict):
        self._mes = mes
        self._dict = _dict
        threading.Thread(target=self.__loadData,
        args=(_dict, )).start()
        
    def __loadData(self, _dict):
        self.get_model().clear()
        iterbase = self.get_model().get_iter_first()
        for item in _dict.items():
            # FIXME: que en la fecha se vea el nombre del dia
            fecha, horas = item
            self.get_model().append(iterbase, [fecha, horas[0], horas[1], horas[2]])

    def __set_columnas(self, cols):
        for col in cols:
            index = cols.index(col)
            cellrender = Gtk.CellRendererText()        
            columna = Gtk.TreeViewColumn(col, cellrender, text=cols.index(col))
            columna.set_property('visible', True)
            columna.set_property('resizable', False)
            self.append_column(columna)
            if index in range(1, 3):
                cellrender.set_property("editable", True)
                cellrender.connect("edited", self.cellrender_edited, cols.index(col))
            else:
                cellrender.set_property("editable", False)

    def cellrender_edited(self, widget, fila, valor, columna):
        col_index = int(columna) - 1
        fil_index = int(fila)
        f = self._dict.keys()[fil_index]
        lista = self._dict[f]
        try:
            tiempo = time.strptime(valor, '%H:%M')
            strtiempo = time.strftime('%H:%M', tiempo)
            if lista[col_index] != strtiempo:
                lista[col_index] = strtiempo
                lista[2] = getDiferenciaHorasMinutos(lista[0], lista[1])
                self._dict[f] = lista
                self.get_model()[fila][columna] = strtiempo
                self.get_model()[fila][3] = lista[2]
                self.emit('updateuser', self._mes, self._dict)
        except:
            return