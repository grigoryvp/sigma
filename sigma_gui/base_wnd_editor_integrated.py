#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import Tkinter

if sys.platform == 'darwin' :
  import Cocoa

import pu
import pmq

##c Code that is shared among windows that can be used as pop-up atop
##  third-party editor (like 'toc' or 'projects').
class WndEditorIntegrated( pu.Wnd ) :

  def __init__( self, parent = None ) :
    pu.Wnd.__init__( self, parent = parent )
    self.bind( '<Escape>', self.__onEscape )
    ##  Used with external editor.
    self.m_fEditor = False

  def m_start( self ) :
    sName = "geometry_{0}".format( self.name() )
    sGeometry = pmq.request( 'm_cfg_get', sName )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256, 256 )
      self.center()

  ##x Overloads |pu.Wnd|.
  def show( self, i_fShow = True ) :
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
      if i_fShow :
        nCx = self.parent().width() / 2
        nCy = self.parent().height() / 2
        nX = self.parent().x() + (self.parent().width() - nCx) / 2
        nY = self.parent().y() + (self.parent().height() - nCy) / 2
        self.transient( master = self.parent() )
        self.geometry( "{0}x{1}+{2}+{3}".format( nCx, nCy, nX, nY ) )
      else :
        self.transient( master = None )
    super( WndEditorIntegrated, self ).show( i_fShow )
    ##  On OSX window will not get focus.
    if i_fShow and sys.platform == 'darwin' :
      Tkinter._default_root.update()
      Cocoa.NSApp.activateIgnoringOtherApps_( Cocoa.YES )

  def m_editor_use( self ) :
    self.m_fEditor = True

  def m_shutdown( self ) :
    sName = "geometry_{0}".format( self.name() )
    pmq.post( 'm_cfg_set', sName, self.geometry() )

  def __onEscape( self, i_oEvent ) :
    self.show( False )
    pmq.post( 'm_{0}_close'.format( self.name() ), self )

