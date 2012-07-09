#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndSettings( pu.Wnd ) :

  def __init__( self, parent = None ) :
    pu.Wnd.__init__( self, parent = parent )
    with pu.Rack( parent = self ) :
      with pu.Spacer() : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Settings" )

  def m_startup( self ) :
    sGeometry = pmq.request( 'm_geometry_get', 'settings' )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256, 256 )
      self.center()

  def m_shutdown( self ) :
    pmq.post( 'm_geometry_set', 'settings', self.geometry() )

