#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndEditor( pu.Wnd ) :

  def __init__( self ) :
    super( WndEditor, self ).__init__()

  def m_startup( self ) :
    sGeometry = pmq.request( 'm_geometry_get', 'editor' )
    if sGeometry :
      self.geometry( sGeometry )

  def m_shutdown( self ) :
    pmq.post( 'm_geometry_set', 'editor', self.geometry() )


