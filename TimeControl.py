#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import datetime

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from MenuBar import MenuBar
from Tabla import Tabla
from TablaSemana import TablaSemana

from Global import adduser
from Global import getDataUser
from Global import addData
from Global import getDataSemana

BASE_PATH = os.path.dirname(__file__)


class TimeControl(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("TimeControl")
        self.set_icon_from_file(
            os.path.join(BASE_PATH, "img", "timecontrol.png"))
        self.set_resizable(True)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        base_hbox = Gtk.HBox()

        self.menuBar = MenuBar()

        self.calendario = Gtk.Calendar()
        self.calendario.connect('day_selected', self.__changed_date)

        frame = Gtk.Frame()
        frame.set_label(' Ingreso de Datos: ')
        frame.set_border_width(15)

        hbox = Gtk.HBox()
        hbox.set_border_width(15)
        self.tabla = Tabla()
        hbox.pack_start(self.tabla, True, False, 0)
        frame.add(hbox)

        vbox = Gtk.VBox()
        vbox.pack_start(self.menuBar, False, False, 0)
        vbox.pack_start(self.calendario, True, False, 0)
        vbox.pack_start(frame, True, False, 0)

        self.tablasemana = TablaSemana()
        base_hbox.pack_start(vbox, True, True, 0)
        base_hbox.pack_start(self.tablasemana, True, True, 0)

        self.add(base_hbox)

        self.connect("delete-event", self.__salir)
        self.menuBar.connect("newuser", self.__newUser)
        self.tabla.connect("viewuser", self.__viewUser)
        self.tabla.connect('save', self.__guardar)
        self.show_all()

    def __guardar(self, widget):
        num, _dict = self.tabla.get_data()
        dialog = Gtk.Dialog(parent=self.get_toplevel(),
        flags=Gtk.DialogFlags.MODAL,
        buttons=["OK", Gtk.ResponseType.OK])
        dialog.set_border_width(15)
        if addData(str(num), _dict):
            label = Gtk.Label("Datos Almacenados.")
            self.__viewUser(None, num)
        else:
            label = Gtk.Label("Este Funcionario no Existe")
        dialog.vbox.pack_start(label, True, True, 5)
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()

    def __get_date_to_string(self):
        res = self.calendario.get_date()
        f = '%s/%s/%s' % (res.day, res.month + 1, res.year)
        fecha = datetime.datetime.strptime(f, '%d/%m/%Y')
        return str(datetime.date.strftime(fecha, '%d/%m/%Y'))

    def __changed_date(self, widget=False):
        self.__viewUser(None, self.tabla.get_data()[0])

    def __viewUser(self, tabla, num):
        fecha = self.__get_date_to_string()
        data = getDataUser(str(num))
        self.tabla.set_data(fecha, num, data)

        semana = datetime.datetime.strptime(
            fecha, '%d/%m/%Y').isocalendar()[1]
        self.tablasemana.set_data(semana, getDataSemana(num, semana, data))

    def __newUser(self, widget, num, name):
        dialog = Gtk.Dialog(parent=self.get_toplevel(),
            flags=Gtk.DialogFlags.MODAL,
            buttons=["OK", Gtk.ResponseType.OK])
        dialog.set_border_width(15)
        if adduser(num, name):
            label = Gtk.Label("Usuario Almacenado")
        else:
            label = Gtk.Label("Este Funcionario ya Existe")
        dialog.vbox.pack_start(label, True, True, 5)
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()
        self.__viewUser(None, num)

    def __salir(self, widget=None, senial=None):
        Gtk.main_quit()
        sys.exit(0)

if __name__ == "__main__":
    jamedia = TimeControl()
    Gtk.main()
