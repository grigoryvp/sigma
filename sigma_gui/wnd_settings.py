#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pu
import pmq

class WndSettings( pu.Wnd ) :

  def __init__( self, parent = None ) :
    pu.Wnd.__init__( self, parent = parent )
    with pu.Rack( parent = self ) :
      with pu.Shelf() :
        with pu.List() :
          pu.o.append( "keybindings", 'keybindings' )
          pu.o.selectByBaton( 'keybindings' )
          pu.o.setGrow( pu.Grow( cx = False, cy = True ) )
          pu.o.setWidth( pixels = pu.o.maxWidth() )
        with pu.Stack() :
          with pu.Rack( 'keybindings') :
            with pu.Label() :
              pu.o.setText( "VIM" )
          pu.o.setCurrent( 'keybindings' )
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Button( 'settings_cancel' ) :
          pu.o.setText( "Cancel" )
        with pu.Button( 'settings_apply' ) :
          pu.o.setText( "Apply" )
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: Settings" )

  def m_start( self ) :
    sName = "geometry_{0}".format( self.name() )
    sGeometry = pmq.request( 'm_cfg_get', sName )
    if sGeometry :
      self.geometry( sGeometry )
    else :
      self.setSize( 256 + 128, 256 )

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
    sName = "geometry_{0}".format( self.name() )
    pmq.post( 'm_cfg_set', sName, self.geometry() )

  def m_on_settings_cancel( self ) :
    self.show( False )

  def m_on_settings_apply( self ) :
    self.show( False )

