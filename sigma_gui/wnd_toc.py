#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys

from base_wnd_editor_integrated import WndEditorIntegrated

import pmq
from pyedsl import pd
import pyuser as pu

class WndToc( WndEditorIntegrated  ) :

  def __init__( self, o_parent = None ) :
    WndEditorIntegrated.__init__( self, o_parent = o_parent )
    with pu.Rack( o_parent = self ) :
      with pu.Stack() as self.m_oStack :
        with pu.Label( s_name = 'info' ) :
          pd.o.setText( "Loading ..." )
          pd.o.alignCenter()
        with pu.List( s_name = 'content' ) :
          self.m_oItems = pd.o
      with pu.StatusBar() : pass
    self.setCaption( "Sigma: TOC" )
    self.keysSetHandler( 'return', self.__onEnter )

  def m_start( self ) :
    ##  Set keybindings mode (VIM, Emacs etc).
    self.o( 'content' ).setKeys( pmq.request( 'm_cfg_get', 'keys' ) )

  def m_toc( self, i_lTags ) :
    self.m_oItems.clear()
    self.show()
    for oTag in i_lTags :
      self.m_oItems.append( s_text = oTag.value(), u_baton = oTag )
    self.m_oStack.setCurrent( 'content' )
    self.m_oItems.setFocus()

  def __onEnter( self ) :
    lItems = self.m_oItems.selection()
    if len( lItems ) :
      pmq.post( 'm_toc_select', self.m_oItems.idToBaton( lItems[ 0 ] ) )
      ##! This will stop app in editor integration mode, see |shutdown|.
      self.close()

