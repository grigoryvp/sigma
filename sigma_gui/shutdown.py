#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq


class Shutdown( pmq.Actor ) :

  def m_wndeditor_close( self ) :
    pmq.stop()

