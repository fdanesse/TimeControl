#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject


class MenuBar(Gtk.MenuBar):

    __gsignals__ = {
        "newuser": (GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING, GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        item = Gtk.MenuItem('Funcionarios')
        self.itemFuncionarios = Gtk.Menu()
        item.set_submenu(self.itemFuncionarios)
        self.append(item)

        nuevo = Gtk.MenuItem('Nuevo . . .')
        nuevo.connect("activate", self.__agregar_funcionario)
        self.itemFuncionarios.append(nuevo)
        self.show_all()

    def __agregar_funcionario(self, widget):
        dialog = Gtk.Dialog(parent=self.get_toplevel(),
            flags=Gtk.DialogFlags.MODAL, buttons=["Guardar",
            Gtk.ResponseType.ACCEPT, "Cancelar", Gtk.ResponseType.CANCEL])
        dialog.set_border_width(15)

        label = Gtk.Label("Ingresa Nº, Nombre y Apellido del Funcionario:")
        dialog.vbox.pack_start(label, True, True, 5)

        hbox = Gtk.HBox()

        frame = Gtk.Frame()
        frame.set_label('Nº')
        event = Gtk.EventBox()
        event.set_border_width(10)
        num = Gtk.Entry()
        num.set_max_width_chars(2)
        num.set_width_chars(2)
        event.add(num)
        frame.add(event)

        hbox.pack_start(frame, False, True, 5)

        frame = Gtk.Frame()
        frame.set_label('Nombre y Apellido')
        event = Gtk.EventBox()
        event.set_border_width(10)
        nombre = Gtk.Entry()  # FIXME: Validation entry.connect('changed', ...)
        event.add(nombre)
        frame.add(event)

        hbox.pack_start(frame, False, True, 5)

        dialog.vbox.pack_start(hbox, False, False, 5)
        dialog.vbox.show_all()

        n = 0
        if dialog.run() == Gtk.ResponseType.ACCEPT:
            try:
                n = int(num.get_text())
                nn = nombre.get_text()
            except:
                print 'FIXME: No se ingresó un número válido'
        dialog.destroy()
        if n and nn:
            self.emit('newuser', n, nn)
