#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import Tkinter

if sys.platform == 'darwin' :
  import Cocoa

import pyuser as pu
import pmq

##c Code that is shared among windows that can be used as pop-up atop
##  third-party editor (like 'toc' or 'projects').
class WndEditorIntegrated( pu.Wnd ) :

  def __init__( self, parent = None ) :
    pu.Wnd.__init__( self, parent = parent )
    self.hotkeyAdd( 'escape', self.close )
    ##  Used with external editor.
    self.m_fEditor = False

  def m_start( self ) :
    sName = "geometry_{0}".format( self.dname )
    sGeometry = pmq.request( 'm_cfg_get', sName )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256, 256 )
      self.center()

  ##x Overloads |pu.Wnd|.
  def show( self, f_show = True ) :
    if self.m_fEditor :
      gGeometry = pmq.request( 'm_editor_geometry_get' )
      if gGeometry is not None :
        nParentX, nParentY, nParentCx, nParentCy = gGeometry
        nCx = nParentCx / 2
        nCy = nParentCy / 2
        nX = nParentX + (nParentCx - nCx) / 2
        nY = nParentY + (nParentCy - nCy) / 2
        self.geometry( "{0}x{1}+{2}+{3}".format( nCx, nCy, nX, nY ) )
    else :
      if f_show :
        nCx = self.dparent.width() / 2
        nCy = self.dparent.height() / 2
        nX = self.dparent.x() + (self.dparent.width() - nCx) / 2
        nY = self.dparent.y() + (self.dparent.height() - nCy) / 2
        self.transient( master = self.dparent )
        self.geometry( "{0}x{1}+{2}+{3}".format( nCx, nCy, nX, nY ) )
      else :
        self.transient( master = None )
    super( WndEditorIntegrated, self ).show( f_show )
    ##  On OSX window will not get focus.
    if f_show and sys.platform == 'darwin' :
      Tkinter._default_root.update()
      Cocoa.NSApp.activateIgnoringOtherApps_( Cocoa.YES )

  def m_editor_use( self ) :
    self.m_fEditor = True

  def m_shutdown( self ) :
    sName = "geometry_{0}".format( self.dname )
    pmq.post( 'm_cfg_set', sName, self.geometry() )

