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

  def m_star( self ) :
    sGeometry = pmq.request( 'm_cfg_get', 'geometry_settings' )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256, 256 )

  ##x Overrides |pu.Wnd.show()|.
  def show( self, i_fShow = True ) :
    if i_fShow :
      self.center()
      self.grab_set()
      self.transient( master = self.parent() )
    else :
      self.grab_release()
      self.transient( master = None )
    super( WndSettings, self ).show( i_fShow )

  def m_wndsettings_close( self ) :
    self.show( False )

  def m_shutdown( self ) :
    pmq.post( 'm_cfg_set', 'geometry_settings', self.geometry() )

