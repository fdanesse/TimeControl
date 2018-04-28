#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from collections import OrderedDict
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from MenuBar import MenuBar
from Notebook import Notebook

from Global import adduser
from Global import getDataUser
from Info import Info

BASE_PATH = os.path.dirname(__file__)


class TimeControl(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("TimeControl")
        self.set_icon_from_file(os.path.join(BASE_PATH, "img", "timecontrol.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.menuBar = MenuBar()
        self.info = Info()
        self.notebook = Notebook()

        panel = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        panel.pack1(self.notebook, resize=True, shrink=False)
        panel.pack2(self.info, resize=False, shrink=True)

        vbox = Gtk.VBox()
        vbox.pack_start(self.menuBar, False, False, 0)
        vbox.pack_start(panel, True, True, 0)

        self.add(vbox)

        self.show_all()

        self.connect("delete-event", self.__salir)
        self.menuBar.connect("adduser", self.__newUser)
        self.menuBar.connect("viewuser", self.__viewUser)

        self._current_user = ''
        self._current_dict = OrderedDict()

        self.notebook.hide() # Se hace visible cuando se cargan los datos
        self.info.frame.hide() # Se hace visible cuando se cargan los datos
        self.info.saldo.hide() # Se hace visible cuando se cargan los datos

        self.notebook.connect('switch_page', self.__switch_page)
        self.notebook.connect('updateuser', self.__update)

    def __update(self, widget, _dict):
        self.info.update(_dict)

    def __switch_page(self, widget, widget_child, indice):
        self.info.switch_page_and_set_user(self._current_user, indice, self._current_dict)

    def __viewUser(self, widget, name):
        self._current_user = name
        self._current_dict = getDataUser(self._current_user)
        self.notebook.set_data(self._current_user, self._current_dict)
        self.info.switch_page_and_set_user(self._current_user, 0, self._current_dict)
        self.notebook.show_all() # Se hace visible cuando se cargan los datos
        self.info.show_all() # Se hace visible cuando se cargan los datos

    def __newUser(self, widget, name):
        if adduser(name):
            self.menuBar.adduser(name)
        else:
            dialog = Gtk.Dialog(parent=self.get_toplevel(),
                flags=Gtk.DialogFlags.MODAL, buttons=["OK", Gtk.ResponseType.OK])
            dialog.set_border_width(15)
            label = Gtk.Label("Este Funcionario ya Existe")
            dialog.vbox.pack_start(label, True, True, 5)
            dialog.vbox.show_all()
            dialog.run()
            dialog.destroy()
        self.__viewUser(None, name)

    def __salir(self, widget=None, senial=None):
        Gtk.main_quit()
        sys.exit(0)

if __name__ == "__main__":
    jamedia = TimeControl()
    Gtk.main()
