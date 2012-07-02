#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndToc( pu.Wnd ) :

  def __init__( self ) :
    super( WndToc, self ).__init__()
    with pu.Rack( parent = self ) :
      with pu.Stack() :
        with pu.Label( name = 'info' ) as this :
          this.setText( "Loading ..." )
          this.alignCenter()
        with pu.List() : pass
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: TOC" )

  def m_startup( self ) :
    sGeometry = pmq.request( 'm_geometry_get', 'toc' )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.center( 256, 256 )

  def m_shutdown( self ) :
    pmq.post( 'm_geometry_set', 'toc', self.geometry() )

