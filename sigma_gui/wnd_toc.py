#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'Table of content' window implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pmq
from pyedsl import pd
import pyuser as pu

class WndToc( WndEditorIntegrated  ):

  def __init__( self, o_parent = None ):
    WndEditorIntegrated.__init__( self, o_parent = o_parent )
    with pu.Rack( o_parent = self ):
      with pu.Stack() as self._stack_o:
        with pu.Label( s_name = 'info' ):
          pd.o.setText( "Loading ..." )
          pd.o.alignCenter()
        with pu.List( s_name = 'content' ):
          self._items_o = pd.o
      with pu.StatusBar(): pass
    self.setCaption( "Sigma: TOC" )
    self.keysSetHandler( 'return', self._onEnter )

  def m_start( self ):
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o( 'content' ).setKeys( pmq.request( 'm_cfg_get', 'keys' ) )

  def m_toc( self, i_lTags ):
    self._items_o.clear()
    self.show()
    for oTag in i_lTags:
      self._items_o.append( s_text = oTag.value(), u_baton = oTag )
    self._stack_o.setCurrent( 'content' )
    self._items_o.setFocus()

  def _onEnter( self ):
    lItems = self._items_o.selection()
    if len( lItems ):
      pmq.post( 'm_toc_select', self._items_o.idToBaton( lItems[ 0 ] ) )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

