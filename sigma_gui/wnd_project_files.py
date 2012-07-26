#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pu
import pmq

class Find( object ) :

  def __init__( self ) :
    self.m_sPattern  = ""
    self.bind( '<Control-f>', self.__onFind )
    self.bind( '<Key>', self.__onKey )

  def __onFind( self, i_oEvent ) :
    self.m_sPattern  = ""
    self.m_oStatus.setText( "/" )

  def __onKey( self, i_oEvent ) :
    if i_oEvent.char :
      self.m_sPattern += i_oEvent.char
      self.m_oStatus.setText( "/{0}".format( self.m_sPattern ) )
      for sFile in self.m_lFiles :
        if self.m_sPattern in sFile :
          self.m_oItems.selectByBaton( sFile )
          break


class WndProjectFiles( WndEditorIntegrated, Find ) :

  def __init__( self ) :
    WndEditorIntegrated.__init__( self )
    Find.__init__( self )
    with pu.Rack( parent = self ) :
      with pu.Stack() as this :
        self.m_oStack = this
        with pu.Label( name = 'info' ) as this :
          self.m_oLabel = this
          this.setText( "Loading ..." )
          this.alignCenter()
        with pu.List( name = 'content' ) as this :
          self.m_oItems = this
      with pu.Shelf() :
        with pu.Label() as this :
          self.m_oStatus = this
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Project files" )
    self.bind( '<Return>', self.__onEnter )

  def m_no_project_set( self ) :
    self.m_oLabel.setText( "Current project not selected" )

  def m_project_no_vcs( self ) :
    self.m_oLabel.setText( "Current project not under VCS" )

  def m_project_files( self, i_lFiles ) :
    self.m_lFiles = i_lFiles
    sCurrent = pmq.request( 'm_project_file_get' )
    self.m_oStatus.setText( "Files: {0}".format( len( self.m_lFiles ) ) )
    for sFile in self.m_lFiles :
      self.m_oItems.append( text = sFile, baton = sFile )
      if sFile == sCurrent :
        self.m_oItems.selectByBaton( sFile )
    self.m_oStack.setCurrent( 'content' )
    self.m_oItems.setFocus()

  def __onEnter( self, i_oEvent ) :
    lItems = self.m_oItems.selection()
    if len( lItems ) :
      pmq.post( 'm_project_file_set', self.m_oItems.idToBaton( lItems[ 0 ] ) )
      pmq.stop()

