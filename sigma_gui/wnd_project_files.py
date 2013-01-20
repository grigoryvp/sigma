#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'Project files' window implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pmq
from pyedsl import pd
import pyuser as pu


class Find( object ) :


  def __init__( self ) :
    self.__sPattern  = None
    self.keysSetHandler( 'ctrl-f', self.__onFind )
    self.keysSetHandler( 'Backspace', self.__onBackspace )


  def __onFind( self, o_event ) :
    ##  Not VIM keybindings?
    if pmq.request( 'm_cfg_get', 'keys' ) != 'vim' :
      self.__sPattern  = ""
      self.o( 'status' ).setText( "/" )


  def __onBackspace( self, o_event ) :
    self.__sPattern = self.__sPattern[ : -1 ]
    self.__redrawList()


  def m_find_on_key( self, o_wnd, o_event ) :
    ##  Not in find mode?
    if self.__sPattern is None :
      ##  VIM keybindings?
      if pmq.request( 'm_cfg_get', 'keys' ) == 'vim' :
        ##  In VIM mode '/' char enters search mode.
        if o_event.char == '/' :
          self.__sPattern  = ""
          self.o( 'status' ).setText( "/" )
    ##  In find mode?
    else :
      if o_event.char :
        self.__sPattern += o_event.char
        self.__redrawList()
      else :
        if o_event.isEnter() :
          self.__onEnter()


  def __redrawList( self ) :
    self.o( 'status' ).setText( "/{0}".format( self.__sPattern ) )
    self.o( 'content' ).clear()
    for sFile in self.m_lFiles :
      if self.__sPattern in sFile :
        self.o( 'content' ).append( s_text = sFile, u_baton = sFile )
        if not self.o( 'content' ).selection() :
          self.o( 'content' ).selectByBaton( sFile )


class WndProjectFiles( WndEditorIntegrated, Find ) :


  def __init__( self, o_parent = None ) :
    WndEditorIntegrated.__init__( self, o_parent = o_parent )
    Find.__init__( self )
    with pu.Rack( o_parent = self ) :
      with pu.Stack( s_name = 'switch' ) :
        with pu.Label( s_name = 'info' ) :
          pd.o.setText( "Loading ..." )
          pd.o.alignCenter()
        with pu.List( s_name = 'content' ) : pass
      with pu.StatusBar( s_name = 'status' ) : pass
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
      self.o( 'content' ).append( s_text = sFile, u_baton = sFile )
      if sFile == sCurrent :
        self.o( 'content' ).selectByBaton( sFile )
    self.o( 'switch' ).setCurrent( 'content' )
    self.o( 'content' ).setFocus()


  def __onEnter( self, o_event ) :
    ##  VIM keybindings?
    if pmq.request( 'm_cfg_get', 'keys' ) == 'vim' :
      ##  In search mode?
      if self.__sPattern is not None :
        ##  If search mode, Enter exits it.
        self.__sPattern  = None
        self.o( 'status' ).setText( "" )
        return
    nId = (self.o( 'content' ).selection() + [ None ])[ 0 ]
    if nId is not None :
      pmq.post( 'm_project_file_set', self.o( 'content' ).idToBaton( nId ) )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

