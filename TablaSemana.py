#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject

from Global import getDiferenciaHorasMinutos
from Global import getTotalHoras

BASE_PATH = os.path.dirname(__file__)


class TablaSemana(Gtk.Frame):

    def __init__(self):
        
        Gtk.Frame.__init__(self)

        self.set_label(' Semana: ')
        self.set_border_width(15)

        self.tabla = Gtk.TreeView(Gtk.ListStore(
            GObject.TYPE_STRING, GObject.TYPE_STRING,
            GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.tabla.set_rules_hint(True)
        self.tabla.set_property("enable-tree-lines", True)
        self.tabla.set_headers_visible(True)
        '''
        cabecera:
            fecha, entrada, salida, saldo
        '''
        self.__set_columnas([
            'Fecha', 'Entrada', 'Salida', 'Saldo'])
        
        vbox = Gtk.VBox()
        vbox.pack_start(self.tabla, True, True, 0)
        self.total = Gtk.Label('Total: 00:00')
        vbox.pack_start(self.total, True, True, 0)

        self.add(vbox)

        self.show_all()

    def __set_columnas(self, cols):
        for col in cols:
            index = cols.index(col)
            cellrender = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(col, cellrender, text=index)
            columna.set_property('visible', True)
            columna.set_property('resizable', False)
            self.tabla.append_column(columna)
            cellrender.set_property("editable", False)
        
    def set_data(self, semana, _dict):
        self.set_label(' Semana: %s ' % semana)
        self.tabla.get_model().clear()
        for key, values in _dict.items():
            self.tabla.get_model().append([key, values[0],
                values[1], getDiferenciaHorasMinutos(values[0], values[1])])
        self.total.set_text('Total: %s' % getTotalHoras(_dict.values()))