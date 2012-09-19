#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import os

import pmq
import sigma
from pyedsl import pd
import pyuser as pu

class WndEditor( pu.Wnd ) :

  def __init__( self ) :
    super( WndEditor, self ).__init__()
    with pu.Menu( parent = self ) :
      with pu.Menu() :
        pd.o.setText( "App" )
        with pu.MenuItem( name = 'settings' ) :
          pd.o.setText( "Settings" )
        with pu.MenuItem( name = 'exit' ) :
          pd.o.setText( "Exit" )
      with pu.Menu() :
        pd.o.setText( "File" )
        with pu.MenuItem( name = 'fopen' ) :
          pd.o.setText( "Open (C-O)" )
      with pu.Menu() :
        pd.o.setText( "Tools" )
        with pu.MenuItem( name = 'toc' ) :
          pd.o.setText( "TOC (C-S-F3)" )
        with pu.MenuItem( name = 'projects' ) :
          pd.o.setText( "Projects (C-S-F9)" )
    with pu.Rack( parent = self ) :
      with pu.Text( name = 'text' ) : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.__updateCaption()
    self.bind( '<Control-o>', lambda _ : self.m_on_fopen() )
    self.bind( '<Control-Shift-F3>', lambda _ : self.m_on_toc() )
    self.bind( '<Control-Shift-F9>', lambda _ : self.m_on_projects() )
    ##  Name of last opened file.
    self.m_sFilename = None
    self.o( 'text' ).setFocus()

  def m_start( self ) :
    sName = "geometry_{0}".format( self.dname )
    sGeometry = pmq.request( 'm_cfg_get', sName )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 512, 384 )
      self.center()
    ##  Try to reopen last file.
    self.m_sFilename = pmq.request( 'm_cfg_get', 'editor_file' )
    if self.m_sFilename is not None :
      if os.path.isfile( self.m_sFilename ) :
        pmq.post( 'm_fopen', self.m_sFilename )
      else :
        pmq.post( 'm_cfg_set', 'editor_file', None )

  def m_shutdown( self ) :
    sName = "geometry_{0}".format( self.dname )
    pmq.post( 'm_cfg_set', sName, self.geometry() )
    if self.m_sFilename is not None :
      pmq.post( 'm_cfg_set', 'editor_file', self.m_sFilename )

  def m_on_exit( self ) :
    pmq.stop()

  def __updateCaption( self, file = None ) :
    if file is None :
      self.setCaption( "Sigma: Editor" )
    else :
      self.setCaption( "Sigma: Editor: \"{0}\"".format( file ) )

  def m_on_fopen( self ) :
    sName = pu.askOpenFileName()
    if sName :
      pmq.post( 'm_fopen', sName )

  def m_on_toc( self ) :
    sText = self.o( 'text' ).getText()
    lTags = [ o for o in sigma.parse( sText ) if o.isToc() ]
    pmq.post( 'm_toc', lTags )

  def m_on_projects( self ) :
    pmq.post( 'm_cmd_projects' )

  def m_toc_select( self, i_oTag ) :
    self.o( 'text' ).mark_set( "insert", "{0}.1".format( i_oTag.line() ) )

  def m_fopen( self, i_sFilename ) :
    try :
      with open( i_sFilename ) as oFile :
        self.o( 'text' ).setText( oFile.read() )
        self.__updateCaption( i_sFilename )
        self.m_sFilename = i_sFilename
    except IOError :
      pu.showMessage( "Failed to open file", type = 'error' )

