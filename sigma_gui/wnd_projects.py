#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

if sys.platform == 'darwin' :
  import Cocoa

import pu
import pmq

class WndProjects( pu.Wnd ) :

  def __init__( self ) :
    pu.Wnd.__init__( self )
    with pu.Rack( parent = self ) :
      with pu.Stack() as this :
        self.m_oStack = this
        with pu.Label( name = 'info' ) as this :
          this.setText( "Loading ..." )
          this.alignCenter()
        with pu.List( name = 'content' ) as this :
          self.m_oItems = this
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Projects" )
    self.bind( '<Return>', self.__onEnter )
    self.bind( '<Escape>', self.__onEscape )
    ##  Used with external editor.
    self.m_fEditor = False

  def m_star( self ) :
    sGeometry = pmq.request( 'm_cfg_get', 'geometry_projects' )
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
    super( WndProjects, self ).show( i_fShow )
    ##  On OSX window will not get focus.
    if i_fShow and sys.platform == 'darwin' :
      pmq.post( 'm_wndprojects_activate' )

  def m_wndprojects_activate( self ) :
    Cocoa.NSApp.activateIgnoringOtherApps_( Cocoa.YES )

  def m_editor_use( self ) :
    self.m_fEditor = True

  def m_shutdown( self ) :
    pmq.post( 'm_cfg_set', 'geometry_projects', self.geometry() )

  def m_projects( self, i_lProjects ) :
    oCurrent = pmq.request( 'm_project_get' )
    for oProject in i_lProjects :
      self.m_oItems.append( text = oProject.name, baton = oProject )
      if oProject == oCurrent :
        self.m_oItems.selectByBaton( oProject )
    self.m_oStack.setCurrent( 'content' )
    self.m_oItems.setFocus()

  def __onEnter( self, i_oEvent ) :
    lItems = self.m_oItems.selection()
    if len( lItems ) :
      pmq.post( 'm_project_set', self.m_oItems.idToBaton( lItems[ 0 ] ) )
      pmq.stop()

  def __onEscape( self, i_oEvent ) :
    pmq.stop()

