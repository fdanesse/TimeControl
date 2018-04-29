#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject

from Global import validateTime
from Global import getDiferenciaHorasMinutos

BASE_PATH = os.path.dirname(__file__)


class Tabla(Gtk.TreeView):

    __gsignals__ = {
        "viewuser": (GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
        "save": (GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE, ())}

    def __init__(self):
        Gtk.TreeView.__init__(self, Gtk.ListStore(
            GObject.TYPE_STRING, GObject.TYPE_INT,
            GObject.TYPE_STRING, GObject.TYPE_STRING,
            GObject.TYPE_STRING, GObject.TYPE_STRING))
        '''
        cabecera:
            fecha, numero, nombre, entrada, salida, saldo
        '''
        self.set_rules_hint(True)
        self.set_property("enable-tree-lines", True)
        self.set_headers_visible(True)
        self.__set_columnas([
            'Fecha', 'Nº', 'Nombre', 'Entrada', 'Salida', 'Saldo'])

        self.get_model().append([None, None, None, None, None, None])
        self.show_all()

    def __set_columnas(self, cols):
        for col in cols:
            index = cols.index(col)
            cellrender = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(col, cellrender, text=index)
            columna.set_property('visible', True)
            columna.set_property('resizable', False)
            self.append_column(columna)

            if col in ['Nº', 'Entrada', 'Salida']:
                cellrender.set_property("editable", True)
            else:
                cellrender.set_property("editable", False)

            if col == 'Nº':
                cellrender.connect('edited', self.__edited_id)
            if col == 'Entrada':
                cellrender.connect('edited', self.__edited_Entrada)
            if col == 'Salida':
                cellrender.connect('edited', self.__edited_Salida)

    def __edited_Entrada(self, widget, _old, _new):
        if not _new:
            return
        val = validateTime(_new)
        if val:
            _iter = self.get_model().get_iter_first()
            self.get_model().set_value(_iter, 3, val)
            self.emit('save')
            self.__calcular_saldo()
        else:
            self.__datosIncorrector()

    def __edited_Salida(self, widget, _old, _new):
        if not _new:
            return
        val = validateTime(_new)
        if val:
            _iter = self.get_model().get_iter_first()
            self.get_model().set_value(_iter, 4, val)
            self.emit('save')
            self.__calcular_saldo()
        else:
            self.__datosIncorrector()

    def __datosIncorrector(self):
        dialog = Gtk.Dialog(parent=self.get_toplevel(),
        flags=Gtk.DialogFlags.MODAL,
        buttons=["OK", Gtk.ResponseType.OK])
        dialog.set_border_width(15)
        label = Gtk.Label("Datos Ingresados Incorrectos")
        dialog.vbox.pack_start(label, True, True, 5)
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()

    def __edited_id(self, widget, _old, num):
        if num:
            try:
                _iter = self.get_model().get_iter_first()
                self.get_model().set_value(_iter, 1, int(num))
                self.emit('viewuser', num)
            except:
                pass

    def __calcular_saldo(self):
        _iter = self.get_model().get_iter_first()
        entrada = self.get_model().get_value(_iter, 3)
        salida = self.get_model().get_value(_iter, 4)
        self.get_model().set_value(_iter, 5,
            getDiferenciaHorasMinutos(entrada, salida))

    def set_data(self, fecha, num, _dict):
        nombre = _dict.get('nombre', '')
        horas = _dict.get('horas', {})
        datafecha = horas.get(fecha, ['00:00', '00:00'])
        _iter = self.get_model().get_iter_first()
        self.get_model().set_value(_iter, 0, fecha)
        self.get_model().set_value(_iter, 1, int(num))
        self.get_model().set_value(_iter, 2, nombre)
        self.get_model().set_value(_iter, 3, datafecha[0])
        self.get_model().set_value(_iter, 4, datafecha[1])
        if not nombre:
            dialog = Gtk.Dialog(parent=self.get_toplevel(),
            flags=Gtk.DialogFlags.MODAL,
            buttons=["OK", Gtk.ResponseType.OK])
            dialog.set_border_width(15)
            label = Gtk.Label("Este Funcionario no Existe")
            dialog.vbox.pack_start(label, True, True, 5)
            dialog.vbox.show_all()
            dialog.run()
            dialog.destroy()
        self.__calcular_saldo()

    def get_data(self):
        _iter = self.get_model().get_iter_first()
        fecha = self.get_model().get_value(_iter, 0)
        num = self.get_model().get_value(_iter, 1)
        _list = [
            self.get_model().get_value(_iter, 3),
            self.get_model().get_value(_iter, 4)]
        return num, {fecha: _list}
