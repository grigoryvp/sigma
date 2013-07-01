#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma user interface: common code for windows that integrates with editors.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import sys
import Tkinter

if sys.platform == 'darwin':
  import Cocoa

import pyuser as pu
import pmq


##c Code that is shared among windows that can be used as pop-up atop
##  third-party editor (like 'toc' or 'projects').
class WndEditorIntegrated( pu.Wnd ):


  def __init__( self, o_parent = None ):
    pu.Wnd.__init__( self, o_parent = o_parent )
    self.keysSetHandler( 'escape', self.close )
    ##  Used with external editor.
    self._editor_f = False


  def m_start( self ):
    sName = "geometry_{0}".format( self.dname )
    lGeometry = pmq.request( 'm_cfg_get', sName )
    if lGeometry:
      self.setGeometry( * lGeometry )
    else:
      self.setSize( 256, 256 )
      self.center()


  ##x Overloads |pu.Wnd|.
  def show( self, f_show = True ):
    if self._editor_f:
      gGeometry = pmq.request( 'm_editor_geometry_get' )
      if gGeometry is not None:
        nParentX, nParentY, nParentCx, nParentCy = gGeometry
        nCx = nParentCx / 2
        nCy = nParentCy / 2
        nX = nParentX + (nParentCx - nCx) / 2
        nY = nParentY + (nParentCy - nCy) / 2
        self.setGeometry( nX, nY, nCx, nCy )
    else:
      if f_show:
        nCx = self.dparent.width() / 2
        nCy = self.dparent.height() / 2
        nX = self.dparent.x() + (self.dparent.width() - nCx) / 2
        nY = self.dparent.y() + (self.dparent.height() - nCy) / 2
        self.setModal()
        self.setGeometry( nX, nY, nCx, nCy )
      else:
        self.setModal( False )
    super( WndEditorIntegrated, self ).show( f_show )
    ##  On OSX window will not get focus.
    if f_show and sys.platform == 'darwin':
      Tkinter._default_root.update()
      Cocoa.NSApp.activateIgnoringOtherApps_( Cocoa.YES )


  def m_editor_use( self ):
    self._editor_f = True


  def m_shutdown( self ):
    sName = "geometry_{0}".format( self.dname )
    pmq.post( 'm_cfg_set', sName, self.geometry() )

