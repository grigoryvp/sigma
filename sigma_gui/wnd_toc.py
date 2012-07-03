#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndToc( pu.Wnd ) :

  def __init__( self ) :
    super( WndToc, self ).__init__()
    with pu.Rack( parent = self ) :
      with pu.Stack() as this :
        self.m_oStack = this
        with pu.Label( name = 'info' ) as this :
          this.setText( "Loading ..." )
          this.alignCenter()
        with pu.List( name = 'content' ) as this :
          self.m_oItems = this
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

  def m_toc( self, i_lTags ) :
    for oTag in i_lTags :
      sId = self.m_oItems.append( text = oTag.value() )
    self.m_oStack.setCurrent( 'content' )
    self.m_oItems.focus_set()

