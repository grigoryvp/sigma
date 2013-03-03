#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: code for VIM editor integration.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

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


  __oGuard = threading.Lock()
  ##  Maps python object ID for object reference to be used as batons in
  ##  native callback. For performance - where is no fast reverse to |id()|.
  __mObjects = {}


  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.__fUse = False
    self.__gEditorGeometry = None


  def m_editor_use( self, s_editor ) :
    if s_editor is not None and "vim" in s_editor.strip() :
      self.__fUse = True


  def m_editor_geometry_get( self ) :
    if self.__fUse :
      pmq.response( self.__gEditorGeometry )


  def m_toc_select( self, o_tag ) :
    if self.__fUse :
      sVimCode = u"".join( [ s.strip() for s in u"""
        <ESC>
        :{line}<CR>
        """.split( u"\n" ) ] ).format( line = o_tag.line() )
      if sys.platform == 'win32' :
        sCmd = "gvim --servername GVIM --remote-send \"{0}\""
      elif sys.platform == 'darwin' :
        ##? Must implement some engine to find executable same way window
        ##  is searched. Window information has PID that can be used to
        ##  find a file.
        sCmd =  "~/apps/MacVim.app/Contents/MacOS/Vim"
        sCmd += " --servername VIM --remote-send \"{0}\""
      else :
        sCmd = "vim --servername GVIM --remote-send \"{0}\""
      sCmd = sCmd.format( sVimCode ).encode( sys.getfilesystemencoding() )
      subprocess.Popen( sCmd, shell = True )
      pmq.stop()


  def m_project_file_set( self, s_file ) :
    if self.__fUse :
      sFile = os.path.join( pmq.request( 'm_project_get' ).dir, s_file )
      sVimCode = u"".join( [ s.strip() for s in u"""
        <ESC>
        :e {file}<CR>
        """.split( u"\n" ) ] ).format( file = sFile )
      if sys.platform == 'win32' :
        sCmd = u"gvim --servername GVIM --remote-send \"{0}\""
      elif sys.platform == 'darwin' :
        ##? Must implement some engine to find executable same way window
        ##  is searched. Window information has PID that can be used to
        ##  find a file.
        sCmd =  u"~/apps/MacVim.app/Contents/MacOS/Vim"
        sCmd += u" --servername VIM --remote-send \"{0}\""
      else :
        sCmd = u"vim --servername GVIM --remote-send \"{0}\""
      sCmd = sCmd.format( sVimCode ).encode( sys.getfilesystemencoding() )
      subprocess.Popen( sCmd, shell = True )
      pmq.stop()


  def m_startup( self ) :
    ##  Get window geometry here - it blocks GUI mainloop.
    self.__gEditorGeometry = self.__wndGeometry()


  def __wndGeometry( self ) :
    if sys.platform == 'win32' :
      @ctypes.WINFUNCTYPE( ctypes.c_int, ctypes.c_int, ctypes.c_int )
      def enumWindowsCallback( i_hWindow, i_nBaton ) :
        with EditorVim.__oGuard :
          if i_nBaton in EditorVim.__mObjects :
            nId = int( i_nBaton )
            EditorVim.__mObjects[ nId ].enumWindowsCallback( i_hWindow )
        return 1
      ##  VIM window handle.
      self.__hWindow = None
      nId = id( self )
      with EditorVim.__oGuard :
        EditorVim.__mObjects[ nId ] = self
      ##  |enumWindowsCallback()| will be called for each window.
      ctypes.windll.user32.EnumWindows( enumWindowsCallback, nId )
      if self.__hWindow is not None :
        oRect = WinapiRect()
        pRect = ctypes.pointer( oRect )
        ctypes.windll.user32.GetWindowRect( self.__hWindow, pRect )
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
      self.__hWindow = i_hWindow


class WinapiRect( ctypes.Structure ) :
  _fields_ = [
    ( "left",   ctypes.c_int ),
    ( "top",    ctypes.c_int ),
    ( "right",  ctypes.c_int ),
    ( "bottom", ctypes.c_int )
  ]

