#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq


class Shutdown( pmq.Actor ) :

  def m_wndeditor_close( self ) :
    pmq.stop()

  ##* If TOC window is displayed as part of complex GUI, closing it
  ##  will close app.
  def m_wndtoc_close( self ) :
    pmq.stop()

  ##* If Projects window is displayed as part of complex GUI, closing it
  ##  will close app.
  def m_wndprojects_close( self ) :
    pmq.stop()

