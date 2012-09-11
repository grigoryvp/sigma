#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pmq
from pyedsl import pd
import pyuser as pu

class WndProjects( WndEditorIntegrated ) :

  def __init__( self ) :
    WndEditorIntegrated.__init__( self )
    with pu.Rack( parent = self ) :
      with pu.Stack() as self.m_oStack :
        with pu.Label( name = 'info' ) :
          pd.o.setText( "Loading ..." )
          pd.o.alignCenter()
        with pu.List( name = 'content' ) : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Projects" )
    self.bind( '<Return>', self.__onEnter )

  def m_start( self ) :
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o( 'content' ).setKeys( pmq.request( 'm_cfg_get', 'keys' ) )

  def m_projects( self, i_lProjects ) :
    oCurrent = pmq.request( 'm_project_get' )
    for oProject in i_lProjects :
      self.o( 'content' ).append( text = oProject.name, baton = oProject )
      if oProject == oCurrent :
        self.o( 'content' ).selectByBaton( oProject )
    self.m_oStack.setCurrent( 'content' )
    self.o( 'content' ).setFocus()

  def __onEnter( self, i_oEvent ) :
    lItems = self.o( 'content' ).selection()
    if len( lItems ) :
      sName = self.o( 'content' ).idToBaton( lItems[ 0 ] )
      pmq.post( 'm_project_set', sName )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

