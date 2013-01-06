#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pmq
from pyedsl import pd
import pyuser as pu

class Find( object ) :

  def __init__( self ) :
    self.m_sPattern  = None
    self.keysSetHandler( 'ctrl-f', self.__onFind )
    self.keysSetHandler( 'Backspace', self.__onBackspace )

  def __onFind( self, i_oEvent ) :
    ##  Not VIM keybindings?
    if pmq.request( 'm_cfg_get', 'keys' ) != 'vim' :
      self.m_sPattern  = ""
      self.o( 'status' ).setText( "/" )

  def __onBackspace( self, i_oEvent ) :
    self.m_sPattern = self.m_sPattern[ : -1 ]
    self.__redrawList()

  def m_find_on_key( self, o_wnd, o_event ) :
    ##  Not in find mode?
    if self.m_sPattern is None :
      ##  VIM keybindings?
      if pmq.request( 'm_cfg_get', 'keys' ) == 'vim' :
        ##  In VIM mode '/' char enters search mode.
        if o_event.char == '/' :
          self.m_sPattern  = ""
          self.o( 'status' ).setText( "/" )
    ##  In find mode?
    else :
      if o_event.char :
        self.m_sPattern += i_oEvent.char
        self.__redrawList()
      else :
        if o_event.isEnter() :
          self.__onEnter()

  def __redrawList( self ) :
    self.o( 'status' ).setText( "/{0}".format( self.m_sPattern ) )
    self.o( 'content' ).clear()
    for sFile in self.m_lFiles :
      if self.m_sPattern in sFile :
        self.o( 'content' ).append( text = sFile, baton = sFile )
        if not self.o( 'content' ).selection() :
          self.o( 'content' ).selectByBaton( sFile )

class WndProjectFiles( WndEditorIntegrated, Find ) :

  def __init__( self, parent = None ) :
    WndEditorIntegrated.__init__( self, parent = parent )
    Find.__init__( self )
    with pu.Rack( parent = self ) :
      with pu.Stack( name = 'switch' ) :
        with pu.Label( name = 'info' ) :
          pd.o.setText( "Loading ..." )
          pd.o.alignCenter()
        with pu.List( name = 'content' ) : pass
      with pu.StatusBar( name = 'status' ) : pass
    self.setCaption( "Sigma: Project files" )

  def m_start( self ) :
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o( 'content' ).setKeys( pmq.request( 'm_cfg_get', 'keys' ) )

  def m_no_project_set( self ) :
    self.o( 'info' ).setText( "Current project not selected" )

  def m_project_no_vcs( self ) :
    self.o( 'info' ).setText( "Current project not under VCS" )

  def m_project_files( self, i_lFiles ) :
    self.show()
    self.m_lFiles = i_lFiles
    sCurrent = pmq.request( 'm_project_file_get' )
    self.o( 'status' ).setText( "Files: {0}".format( len( self.m_lFiles ) ) )
    for sFile in self.m_lFiles :
      self.o( 'content' ).append( text = sFile, baton = sFile )
      if sFile == sCurrent :
        self.o( 'content' ).selectByBaton( sFile )
    self.o( 'switch' ).setCurrent( 'content' )
    self.o( 'content' ).setFocus()

  def __onEnter( self, i_oEvent ) :
    ##  VIM keybindings?
    if pmq.request( 'm_cfg_get', 'keys' ) == 'vim' :
      ##  In search mode?
      if self.m_sPattern is not None :
        ##  If search mode, Enter exits it.
        self.m_sPattern  = None
        self.o( 'status' ).setText( "" )
        return
    nId = (self.o( 'content' ).selection() + [ None ])[ 0 ]
    if nId is not None :
      pmq.post( 'm_project_file_set', self.o( 'content' ).idToBaton( nId ) )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

