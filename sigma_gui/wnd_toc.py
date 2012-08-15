#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pu
import pmq

class WndToc( WndEditorIntegrated  ) :

  def __init__( self ) :
    WndEditorIntegrated.__init__( self )
    with pu.Rack( parent = self ) :
      with pu.Stack() :
        self.m_oStack = pu.o
        with pu.Label( name = 'info' ) :
          pu.o.setText( "Loading ..." )
          pu.o.alignCenter()
        with pu.List( name = 'content' ) :
          self.m_oItems = pu.o
      with pu.Shelf() :
        with pu.Spacer() : pass
        with pu.Grip() : pass
    self.setCaption( "Sigma: TOC" )
    self.bind( '<Return>', self.__onEnter )

  def m_start( self ) :
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o[ 'content' ].setKeys( pmq.request( 'm_cfg_get', 'keys' ) )

  def m_toc( self, i_lTags ) :
    for oTag in i_lTags :
      self.m_oItems.append( text = oTag.value(), baton = oTag )
    self.m_oStack.setCurrent( 'content' )
    self.m_oItems.setFocus()

  def __onEnter( self, i_oEvent ) :
    lItems = self.m_oItems.selection()
    if len( lItems ) :
      pmq.post( 'm_toc_select', self.m_oItems.idToBaton( lItems[ 0 ] ) )
      pmq.stop()

