#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndEditor( pu.Wnd ) :

  def __init__( self ) :
    super( WndEditor, self ).__init__()
    with pu.Rack( parent = self ) :
      with pu.Text() : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Editor" )

  def m_startup( self ) :
    sGeometry = pmq.request( 'm_geometry_get', 'editor' )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.center( 256, 256 )

  def m_shutdown( self ) :
    pmq.post( 'm_geometry_set', 'editor', self.geometry() )

