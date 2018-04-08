#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject

from Global import getUsers


class MenuBar(Gtk.MenuBar):

    __gsignals__ = {
        "adduser": (GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
        "viewuser": (GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        #self.modify_bg(0, get_colors("window"))
        
        item = Gtk.MenuItem('Funcionarios')
        self.itemFuncionarios = Gtk.Menu()
        item.set_submenu(self.itemFuncionarios)
        self.append(item)

        nuevo = Gtk.MenuItem('Nuevo . . .')
        nuevo.connect("activate", self.__agregar_funcionario)
        self.itemFuncionarios.append(nuevo)
    
        self.__setUsers()
        self.show_all()

    def adduser(self, name):
        nuevo = Gtk.MenuItem(name)
        nuevo.connect("activate", self.__view_funcionario, name)
        self.itemFuncionarios.append(nuevo)
        self.show_all()

    def __setUsers(self):
        funcionarios =  getUsers() # lista de nombres de archivos
        for funcionario in funcionarios:
            nuevo = Gtk.MenuItem(funcionario)
            nuevo.connect("activate", self.__view_funcionario, funcionario)
            self.itemFuncionarios.append(nuevo)

    def __view_funcionario(self, widget, funcionario):
        self.emit('viewuser', funcionario)

    def __agregar_funcionario(self, widget):
        dialog = Gtk.Dialog(parent=self.get_toplevel(),
            flags=Gtk.DialogFlags.MODAL, buttons=["Guardar",
            Gtk.ResponseType.ACCEPT, "Cancelar", Gtk.ResponseType.CANCEL])
        dialog.set_border_width(15)

        label = Gtk.Label("Ingresa Nombre y Apellido del Funcionario:")
        entry = Gtk.Entry()
        # FIXME: Validation entry.connect('changed', ...)
        dialog.vbox.pack_start(label, True, True, 5)
        dialog.vbox.pack_start(entry, True, True, 5)
        dialog.vbox.show_all()
        
        text = '' # Para que no se superpongan dialogs
        if dialog.run() == Gtk.ResponseType.ACCEPT:
            text = entry.get_text()
        dialog.destroy()
        if text: self.emit('adduser', text)