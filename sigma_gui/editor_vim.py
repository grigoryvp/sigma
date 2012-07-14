#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import sys
import os
import ctypes
import subprocess
import threading

if sys.platform == 'linux2' :
  import gtk.gdk
if sys.platform == 'darwin' :
  import Cocoa
  import Quartz

import pmq
import os

##c Communication with VIM editor.
class EditorVim( pmq.Actor ) :

  m_oGuard = threading.Lock()
  ##  Maps python object ID for object reference to be used as batons in
  ##  native callback. For performance - where is no fast reverse to |id()|.
  m_mObjects = {}

  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.m_fUse = False
    self.m_gEditorGeometry = None

  def m_editor_use( self, i_sEditor ) :
    if i_sEditor is not None and "vim" in i_sEditor.strip() :
      self.m_fUse = True

  def m_editor_geometry_get( self ) :
    if self.m_fUse :
      pmq.response( self.m_gEditorGeometry )

  def m_toc_select( self, i_oTag ) :
    if self.m_fUse :
      if sys.platform == 'win32' :
        sCmd = "gvim --servername GVIM --remote-send \"<ESC>:{0}<CR>\""
      elif sys.platform == 'darwin' :
        ##* Must implement some engine to find executable same way window
        ##  is searched. Window information has PID that can be used to
        ##  find a file.
        sCmd =  "~/apps/MacVim.app/Contents/MacOS/Vim"
        sCmd += " --servername VIM --remote-send \"<ESC>:{0}<CR>\""
      else :
        sCmd = "vim --servername GVIM --remote-send \"<ESC>:{0}<CR>\""
      subprocess.Popen( sCmd.format( i_oTag.line() ), shell = True )
      pmq.stop()

  def m_startup( self ) :
    ##  Get window geometry here - it blocks GUI mainloop.
    self.m_gEditorGeometry = self.__wndGeometry()

  def __wndGeometry( self ) :
    if sys.platform == 'win32' :
      @ctypes.WINFUNCTYPE( ctypes.c_int, ctypes.c_int, ctypes.c_int )
      def enumWindowsCallback( i_hWindow, i_nBaton ) :
        with EditorVim.m_oLock() :
          if i_nBaton in EditorVim.m_mObjects :
            EditorVim.m_mObjects[ i_nBaton ].enumWindowsCallback( i_hWindow )
        return 1
      ##  VIM window handle.
      self.m_hWindow = None
      with EditorVim.m_oLock() :
        nId = ctypes.c_int( id( self ) )
        EditorVim.m_mObjects[ nId ] = self
      ##  |enumWindowsCallback()| will be called for each window.
      ctypes.windll.user32.EnumWindows( enumWindowsCallback, nId )
      if self.m_hWindow is not None :
        oRect = WinapiRect()
        pRect = ctypes.pointer( oRect )
        ctypes.windll.user32.GetWindowRect( self.m_hWindow, pRect )
        nCx = oRect.right - oRect.left
        nCy = oRect.bottom - oRect.top
        return oRect.left, oRect.top, nCx, nCy
    if sys.platform == 'linux2' :
      oWndRoot = gtk.gdk.get_default_root_window()
      _, _, lChildIds = oWndRoot.property_get( '_NET_CLIENT_LIST' )
      for nId in lChildIds :
        oWndApp = gtk.gdk.window_foreign_new( nId )
        gName = oWndApp.property_get( '_NET_WM_NAME' )
        if gName is not None :
          _, _, sName = gName
          if sName.endswith( "- GVIM" ) :
            nX, nY = oWndApp.get_origin()
            nCx, nCy = oWndApp.get_size()
            return nX, nY, nCx, nCy
    if sys.platform == 'darwin' :
      oPool = Cocoa.NSAutoreleasePool.alloc().init()
      for mWinInfo in Quartz.CGWindowListCopyWindowInfo( 0, 0 ) :
        if Quartz.kCGWindowName in mWinInfo :
          if mWinInfo[ Quartz.kCGWindowName ].endswith( "- VIM" ) :
            nX = int( mWinInfo[ Quartz.kCGWindowBounds ][ 'X' ] )
            nY = int( mWinInfo[ Quartz.kCGWindowBounds ][ 'Y' ] )
            nCx = int( mWinInfo[ Quartz.kCGWindowBounds ][ 'Width' ] )
            nCy = int( mWinInfo[ Quartz.kCGWindowBounds ][ 'Height' ] )
            return nX, nY, nCx, nCy

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

