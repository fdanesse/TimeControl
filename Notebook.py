#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GObject

from Tree import Tree
from Global import updateUser


class Notebook(Gtk.Notebook):

    __gsignals__ = {
        "updateuser": (GObject.SIGNAL_RUN_FIRST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING,
            GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.Notebook.__init__(self)
        self.set_scrollable(True)
        self.__make_pages([
            'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
            'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre'])
        self.show_all()

        self._user = ''
        self._dict = {}

    def set_data(self, user, _dict):
        self._user = user
        self._dict = _dict
        paginas = self.get_children()
        for pag in paginas:
            index = paginas.index(pag)
            scrolled = paginas[index]
            tree = scrolled.get_children()[0]
            # index+3 porque comenzamos en marzo
            tree.set_data_mes(user, index+3, _dict.get(str(index+3), False))

    def __cerrar(self, widget):
        # FIXME: los indices en set_data no se corresponden luego de cerrar alguna lengueta
        pass
        '''
        paginas = self.get_n_pages()
        for indice in range(paginas):
            boton = self.get_tab_label(self.get_children()[indice]).get_children()[1]
            if boton == widget:
                pagina = self.get_children()[indice]
                self.remove(pagina)
                pagina.destroy()
                break
        '''

    def __make_pages(self, meses):
        for mes in meses:
            hbox = Gtk.HBox()
            label = Gtk.Label(mes)
            boton = Gtk.ToolButton(Gtk.STOCK_CLOSE)
            boton.connect("clicked", self.__cerrar)
            hbox.pack_start(label, False, False, 0)
            #hbox.pack_start(boton, False, False, 0)
            tree = Tree()
            scroll = Gtk.ScrolledWindow()
            scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            scroll.add(tree)
            self.append_page(scroll, hbox)
            hbox.show_all()
            tree.connect('updateuser', self.__updateUser)
        self.show_all()

    def __updateUser(self, widget, mes, _dict):
        self._dict[mes] = _dict
        updateUser(self._user, self._dict)
        self.emit('updateuser', self._dict)