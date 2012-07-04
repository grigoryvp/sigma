#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import ctypes
import gc

import pmq
import os

##c Communication with VIM editor.
class EditorVim( pmq.Actor ) :

  m_oCommand = None
  m_fUse = False

  def m_editor_use( self, i_sEditor ) :
    if i_sEditor is not None and "vim" in i_sEditor.strip() :
      EditorVim.m_fUse = True

  def m_editor_geometry_get( self ) :
    if EditorVim.m_fUse :
      pmq.post( 'm_editor_geometry', self.__wndGeometry() )

  def m_toc_select( self, i_oTag ) :
    if EditorVim.m_fUse :
      EditorVim.m_oCommand = CommandToc( i_oTag.line() )

  @classmethod
  def TryHandleCommand( self ) :
    if self.m_fUse and self.m_oCommand is not None :
      self.m_oCommand.handle()

  def __wndGeometry( self ) :
    if sys.platform == 'win32' :
      ##  VIM window handle.
      self.m_hWindow = None
      nId = ctypes.c_int( id( self ) )
      ##  |enumWindowsCallback()| will be called for each window.
      ctypes.windll.user32.EnumWindows( enumWindowsCallback, nId )
      if self.m_hWindow is not None :
        oRect = WinapiRect()
        pRect = ctypes.pointer( oRect )
        ctypes.windll.user32.GetWindowRect( self.m_hWindow, pRect )
        nCx = oRect.right - oRect.left
        nCy = oRect.bottom - oRect.top
        return oRect.left, oRect.top, nCx, nCy

  def enumWindowsCallback( self, i_hWindow ) :
    nNameMax = 256
    aName = (ctypes.c_wchar * nNameMax)()
    ctypes.windll.user32.GetWindowTextW(
      ctypes.c_int( i_hWindow ),
      aName,
      ctypes.c_int( nNameMax ) )
    if aName.value.endswith( "- GVIM" ) :
      self.m_hWindow = i_hWindow


class WinapiRect( ctypes.Structure ) :
  _fields_ = [
    ( "left",   ctypes.c_int ),
    ( "top",    ctypes.c_int ),
    ( "right",  ctypes.c_int ),
    ( "bottom", ctypes.c_int )
  ]

@ctypes.WINFUNCTYPE( ctypes.c_int, ctypes.c_int, ctypes.c_int )
def enumWindowsCallback( i_hWindow, i_nBaton ) :
  oInstance = [ o for o in gc.get_objects() if id( o ) == i_nBaton ][ 0 ]
  oInstance.enumWindowsCallback( i_hWindow )
  return 1


class Command( object ) :
  pass


class CommandToc( Command ) :

  def __init__( self, line ) :
    self.m_nLine = line

  def handle( self ) :
    sCmd = "vim --servername GVIM --remote-send \"<ESC>:{0}<CR>\""
    os.system( sCmd.format( self.m_nLine ) )

