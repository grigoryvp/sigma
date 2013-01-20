#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'Projects' window implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import sys
import os
import itertools
import Tkinter

from base_wnd_editor_integrated import WndEditorIntegrated

import pmq
from pyedsl import pd
import pyuser as pu


class WndProjects( WndEditorIntegrated ) :


  def __init__( self, o_parent = None ) :
    WndEditorIntegrated.__init__( self, o_parent = o_parent )
    with pu.Rack( o_parent = self ) :
      with pu.Stack( s_name = 'stack' ) :
        with pu.Label( s_name = 'info' ) :
          pd.o.setText( "Loading ..." )
          pd.o.alignCenter()
        with pu.List( s_name = 'content' ) : pass
      with pu.StatusBar() : pass
    self.setCaption( "Sigma: Projects" )
    self.keysSetHandler( 'return', self.__onEnter )
    self.__mImg = {}
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
      self.__mImg[ sId ] = oImg


  def m_start( self ) :
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o( 'content' ).setKeys( pmq.request( 'm_cfg_get', 'keys' ) )


  def m_projects( self, l_projects ) :
    self.show()
    oCurrent = pmq.request( 'm_project_get' )
    oContent = self.o( 'content' )
    oContent.clear()
    for oProject in l_projects :
      oContent.append( s_text = oProject.name, u_baton = oProject )
      oImg = self.__mImg[ 'nonscanned' ]
      oContent.itemImageSet( oContent.batonToId( oProject ), oImg )
      if oProject == oCurrent :
        oContent.selectByBaton( oProject )
    self.o( 'stack' ).setCurrent( 'content' )
    oContent.setFocus()


  def m_project_status_updated( self, o_project ) :
    oContent = self.o( 'content' )
    sStatus = 'unknown'
    if o_project.commited == 'no' :
      if o_project.pulled == 'no' :
        sStatus = 'uncommited_unpulled'
      elif o_project.pulled == 'yes' :
        sStatus = 'uncommited_pulled'
      else :
        sStatus = 'uncommited_unknown'
    else :
      if o_project.pushed == 'no' :
        if o_project.pulled == 'no' :
          sStatus = 'unpushed_unpulled'
        elif o_project.pulled == 'yes' :
          sStatus = 'unpushed_pulled'
      elif o_project.pushed == 'yes' :
        if o_project.pulled == 'no' :
          sStatus = 'pushed_unpulled'
        elif o_project.pulled == 'yes' :
          sStatus = 'pushed_pulled'
    oImg = self.__mImg[ sStatus ]
    oContent.itemImageSet( oContent.batonToId( o_project ), oImg )


  def __onEnter( self ) :
    lItems = self.o( 'content' ).selection()
    if len( lItems ) :
      sName = self.o( 'content' ).idToBaton( lItems[ 0 ] )
      pmq.post( 'm_project_set', sName )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

