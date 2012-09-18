#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import os
import itertools
import Tkinter

from base_wnd_editor_integrated import WndEditorIntegrated

import pmq
from pyedsl import pd
import pyuser as pu

class WndProjects( WndEditorIntegrated ) :

  def __init__( self, parent = None ) :
    WndEditorIntegrated.__init__( self, parent = parent )
    with pu.Rack( parent = self ) :
      with pu.Stack( name = 'stack' ) :
        with pu.Label( name = 'info' ) :
          pd.o.setText( "Loading ..." )
          pd.o.alignCenter()
        with pu.List( name = 'content' ) : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Projects" )
    self.bind( '<Return>', self.__onEnter )
    self.m_mImg = {}
    lStatesOut = [ 'pushed', 'unpushed', 'uncommited' ]
    lStatesIn = [ 'pulled', 'unpulled' ]
    for lCombination in itertools.product( lStatesOut, lStatesIn ) :
      sId = '_'.join( lCombination )
      sFile = os.path.join( sys.path[ -1 ], 'res', '{0}.gif'.format( sId ) )
      oImg = Tkinter.PhotoImage( file = sFile )
      self.m_mImg[ sId ] = oImg
      self.o( 'content' ).tag_configure( sId, image = oImg )

  def m_start( self ) :
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o( 'content' ).setKeys( pmq.request( 'm_cfg_get', 'keys' ) )

  def m_projects( self, i_lProjects ) :
    self.show()
    oCurrent = pmq.request( 'm_project_get' )
    oContent = self.o( 'content' )
    for oProject in i_lProjects :
      oContent.append( text = oProject.name, baton = oProject )
      oContent.itemTagSet( baton = oProject, tag = 'pushed_pulled' )
      if oProject == oCurrent :
        oContent.selectByBaton( oProject )
    self.o( 'stack' ).setCurrent( 'content' )
    oContent.setFocus()

  def m_project_status_updated( self, i_oProject ) :
    oContent = self.o( 'content' )
    if i_oProject.commited == False :
      oContent.itemTagSet( baton = i_oProject, tag = 'uncommited_pulled' )
    else :
      oContent.itemTagSet( baton = i_oProject, tag = 'pushed_pulled' )

  def __onEnter( self, i_oEvent ) :
    lItems = self.o( 'content' ).selection()
    if len( lItems ) :
      sName = self.o( 'content' ).idToBaton( lItems[ 0 ] )
      pmq.post( 'm_project_set', sName )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

