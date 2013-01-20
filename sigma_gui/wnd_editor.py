#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'Editor' window implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import os

import pmq
import sigma
from pyedsl import pd
import pyuser as pu


class WndEditor( pu.Wnd ) :


  def __init__( self ) :
    super( WndEditor, self ).__init__()
    with pu.MenuBar( o_parent = self ) :
      with pu.Menu() :
        pd.o.setText( "App" )
        with pu.MenuItem( s_name = 'settings' ) :
          pd.o.setText( "Settings" )
        with pu.MenuItem( s_name = 'exit' ) :
          pd.o.setText( "Exit" )
      with pu.Menu() :
        pd.o.setText( "File" )
        with pu.MenuItem( s_name = 'fopen' ) :
          pd.o.setText( "Open (C-O)" )
      with pu.Menu() :
        pd.o.setText( "Tools" )
        with pu.MenuItem( s_name = 'workspace' ) :
          pd.o.setText( "Workspace (C-S-F1)" )
        with pu.MenuItem( s_name = 'toc' ) :
          pd.o.setText( "TOC (C-S-F3)" )
        with pu.MenuItem( s_name = 'projects' ) :
          pd.o.setText( "Projects (C-S-F9)" )
    with pu.Rack( o_parent = self ) :
      with pu.Text( s_name = 'text' ) : pass
      with pu.StatusBar() : pass
    self.__updateCaption()
    self.keysSetHandler( 'ctrl-o', self.m_on_fopen )
    self.keysSetHandler( 'ctrl-shift-f1', self.m_on_workspace )
    self.keysSetHandler( 'ctrl-shift-f3', self.m_on_toc )
    self.keysSetHandler( 'ctrl-shift-f9', self.m_on_projects )
    ##  Name of last opened file.
    self.__sFilename = None
    self.o( 'text' ).setFocus()


  def m_start( self ) :
    sName = "geometry_{0}".format( self.dname )
    lGeometry = pmq.request( 'm_cfg_get', sName )
    if lGeometry :
      self.setGeometry( * lGeometry )
    else :
      self.setSize( 512, 384 )
      self.center()
    ##  Try to reopen last file.
    self.__sFilename = pmq.request( 'm_cfg_get', 'editor_file' )
    if self.__sFilename is not None :
      if os.path.isfile( self.__sFilename ) :
        pmq.post( 'm_fopen', self.__sFilename )
      else :
        pmq.post( 'm_cfg_set', 'editor_file', None )


  def m_shutdown( self ) :
    sName = "geometry_{0}".format( self.dname )
    pmq.post( 'm_cfg_set', sName, self.geometry() )
    if self.__sFilename is not None :
      pmq.post( 'm_cfg_set', 'editor_file', self.__sFilename )


  def m_on_exit( self ) :
    pmq.stop()


  def __updateCaption( self, s_file = None ) :
    if s_file is None :
      self.setCaption( "Sigma: Editor" )
    else :
      self.setCaption( "Sigma: Editor: \"{0}\"".format( s_file ) )


  def m_on_fopen( self ) :
    sName = pu.askOpenFileName()
    if sName :
      pmq.post( 'm_fopen', sName )


  def m_on_workspace( self ) :
    pmq.post( 'm_cmd_project_files' )


  def m_on_toc( self ) :
    sText = self.o( 'text' ).getText()
    if sText :
      lTags = [ o for o in sigma.parse( sText ) if o.isToc() ]
      pmq.post( 'm_toc', lTags )


  def m_on_projects( self ) :
    pmq.post( 'm_cmd_projects' )


  def m_toc_select( self, o_tag ) :
    self.o( 'text' ).mark_set( "insert", "{0}.1".format( o_tag.line() ) )


  def m_project_file_set( self, s_subpath ) :
    oProject = pmq.request( 'm_project_get' )
    if oProject is not None :
      self.__fopen( os.path.join( oProject.dir, s_subpath ) )


  def m_fopen( self, s_filename ) :
    try :
      with open( s_filename ) as oFile :
        self.o( 'text' ).setText( oFile.read() )
        self.__updateCaption( s_filename )
        self.__sFilename = s_filename
        self.o( 'text' ).setCaret( 0, 0 )
        self.o( 'text' ).setFocus()
    except IOError :
      pu.showMessage( "Failed to open file", type = 'error' )

