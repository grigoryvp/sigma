#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: GUI shutdown sequence implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pmq


class Shutdown( pmq.Actor ):


  def __init__( self ):
    pmq.Actor.__init__( self )
    ##  True if working as GUI for some external editor.
    self._editor_f = False


  def m_wndeditor_close( self ):
    pmq.stop()


  def m_wndtoc_close( self ):
    if self._editor_f:
      pmq.stop()


  def m_wndprojects_close( self ):
    if self._editor_f:
      pmq.stop()


  def m_wndprojectfiles_close( self ):
    if self._editor_f:
      pmq.stop()


  def m_editor_use( self ):
    self._editor_f = True

