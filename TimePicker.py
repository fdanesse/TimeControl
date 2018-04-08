#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class TimePicker(Gtk.VBox):
    def __init__(self):
        super(TimePicker, self).__init__()
        sp_h_adj = Gtk.Adjustment(0, 0, 24, 1, 10, 0)
        self.sp_h = Gtk.SpinButton(sp_h_adj, 1, 0)
        self.sp_h.set_numeric(True)
        self.sp_h.set_size_request(50, 27)

        sp_m_adj = Gtk.Adjustment(0, 0, 59, 1, 10, 0)
        self.sp_m = Gtk.SpinButton(sp_m_adj, 1, 0)
        self.sp_m.set_numeric(True)
        self.sp_m.set_size_request(45, 27)

        sp_s_adj = Gtk.Adjustment(0, 0, 59, 1, 10, 0)
        self.sp_s = Gtk.SpinButton(sp_s_adj, 1, 0)
        self.sp_s.set_numeric(True)
        self.sp_s.set_size_request(45, 27)

        box = Gtk.HBox()
        box.pack_start(self.sp_h, False)
        box.pack_start(self.sp_m, False)
        box.pack_start(self.sp_s, False)

        self.pack_start(box, False)
        self.show_all()

    def get_time(self):
        """Start choosen process"""
        # Get spinbutton values as int, calculate total and current time
        h = self.sp_h.get_value_as_int()
        m = self.sp_m.get_value_as_int()
        s = self.sp_s.get_value_as_int()

        t = datetime.time(h, m, s)
        return t
    
    def set_time(self, time):
        self.sp_h.set_value(time.hour)
        self.sp_m.set_value(time.minute)
        self.sp_s.set_value(time.second)