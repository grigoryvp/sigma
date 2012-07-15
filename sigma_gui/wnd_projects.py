#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pu
import pmq

class WndProjects( WndEditorIntegrated ) :

  def __init__( self ) :
    WndEditorIntegrated.__init__( self )
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

