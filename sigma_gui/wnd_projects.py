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
    self.hotkeyAdd( 'return', self.__onEnter )
    self.m_mImg = {}
    lOut = [ 'pushed', 'unpushed', 'uncommited' ]
    lIn = [ 'pulled', 'unpulled' ]
    lIds = [ '_'.join( s ) for s in itertools.product( lOut, lIn ) ]
    ##  Project status is not scanned yet.
    lIds.append( 'nonscanned' )
    ##  Project status is scanned and is unknown: no VCS, offline etc.
    lIds.append( 'unknown' )
    ##  Project status is partially scanned (local commit status detected,
    ##  other info unavailable - probably offline).
    lIds.append( 'uncommited_unknown' )
    for sId in lIds :
      sFile = os.path.join( sys.path[ -1 ], 'res', '{0}.gif'.format( sId ) )
      oImg = pu.Image( s_file = sFile )
      self.m_mImg[ sId ] = oImg

  def m_start( self ) :
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o( 'content' ).setKeys( pmq.request( 'm_cfg_get', 'keys' ) )

  def m_projects( self, i_lProjects ) :
    self.show()
    oCurrent = pmq.request( 'm_project_get' )
    oContent = self.o( 'content' )
    for oProject in i_lProjects :
      oContent.append( text = oProject.name, baton = oProject )
      oContent.itemTagSet( baton = oProject, tag = 'nonscanned' )
      if oProject == oCurrent :
        oContent.selectByBaton( oProject )
    self.o( 'stack' ).setCurrent( 'content' )
    oContent.setFocus()

  def m_project_status_updated( self, i_oProject ) :
    oContent = self.o( 'content' )
    sStatus = 'unknown'
    if i_oProject.commited == 'no' :
      if i_oProject.pulled == 'no' :
        sStatus = 'uncommited_unpulled'
      elif i_oProject.pulled == 'yes' :
        sStatus = 'uncommited_pulled'
      else :
        sStatus = 'uncommited_unknown'
    else :
      if i_oProject.pushed == 'no' :
        if i_oProject.pulled == 'no' :
          sStatus = 'unpushed_unpulled'
        elif i_oProject.pulled == 'yes' :
          sStatus = 'unpushed_pulled'
      elif i_oProject.pushed == 'yes' :
        if i_oProject.pulled == 'no' :
          sStatus = 'pushed_unpulled'
        elif i_oProject.pulled == 'yes' :
          sStatus = 'pushed_pulled'
    oContent.itemTagSet( baton = i_oProject, tag = sStatus )

  def __onEnter( self ) :
    lItems = self.o( 'content' ).selection()
    if len( lItems ) :
      sName = self.o( 'content' ).idToBaton( lItems[ 0 ] )
      pmq.post( 'm_project_set', sName )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

