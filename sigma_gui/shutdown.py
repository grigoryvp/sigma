#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq


class Shutdown( pmq.Actor ) :

  def __init__( self ) :
    pmq.Actor.__init__( self )
    ##  True if working as GUI for some external editor.
    self.m_fEditor = False

  def m_wndeditor_close( self ) :
    pmq.stop()

  def m_wndtoc_close( self ) :
    if self.m_fEditor :
      pmq.stop()

  def m_wndprojects_close( self ) :
    if self.m_fEditor :
      pmq.stop()

  def m_wndprojectfiles_close( self ) :
    if self.m_fEditor :
      pmq.stop()

  def m_editor_use( self ) :
    self.m_fEditor = True

