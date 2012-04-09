#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

from Tkinter import *
from ttk import *

import wnd_editor

##  Singleton object.
oRoot = Tk()
oRoot.withdraw()

oWnd = WndEditor()

oRoot.mainloop()

