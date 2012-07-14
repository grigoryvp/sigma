#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndEditor( pu.Wnd ) :

  def __init__( self ) :
    super( WndEditor, self ).__init__()
    with pu.Menu( parent = self ) :
      with pu.Menu() as this :
        this.setText( "App" )
        with pu.MenuItem( name = 'settings' ) as this :
          this.setText( "Settings" )
        with pu.MenuItem( name = 'exit' ) as this :
          this.setText( "Exit" )
    with pu.Rack( parent = self ) :
      with pu.Text() : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Editor" )

  def m_start( self ) :
    sGeometry = pmq.request( 'm_geometry_get', 'editor' )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256, 256 )
      self.center()

  def m_shutdown( self ) :
    pmq.post( 'm_geometry_set', 'editor', self.geometry() )

  def m_on_exit( self ) :
    pmq.stop()

