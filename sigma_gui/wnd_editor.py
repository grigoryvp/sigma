#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

from Tkinter import *
from ttk import *

class WndEditor( Toplevel ) :

  def __init__( self ) :
    super( WndEditor, self ).__init__( Tk() )
    self.withdraw()

