#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq
import os

##c Communication with VIM editor.
class EditorVim( pmq.Actor ) :

  m_oCommand = None
  m_fUse = False

  def m_editor_use( self, i_sEditor ) :
    if i_sEditor is not None and "vim" in i_sEditor.strip() :
      EditorVim.m_fUse = True

  def m_toc_select( self, i_oTag ) :
    if EditorVim.m_fUse :
      EditorVim.m_oCommand = CommandToc( i_oTag.line() )

  @classmethod
  def TryHandleCommand( self ) :
    if self.m_fUse and self.m_oCommand is not None :
      self.m_oCommand.handle()


class Command( object ) :
  pass


class CommandToc( Command ) :

  def __init__( self, line ) :
    self.m_nLine = line

  def handle( self ) :
    sCmd = "vim --servername GVIM --remote-send \"<ESC>:{0}<CR>\""
    os.system( sCmd.format( self.m_nLine ) )

