#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import argparse

import pmq

class Commandline( pmq.Actor ) :

  def m_commandline_handle( self ) :
    try :
      print( "1" )
      oParses = argparse.ArgumentParser( description = "Sigma" )
      print( "2" )
      sHelp = "Editor to interact"
      print( "3" )
      lEditors = [ 'vim' ]
      oParses.add_argument( '-editor', help = sHelp, choices = lEditors )
      oArgs = oParses.parse_args()
      print( "4" )
      pmq.post( 'm_wndeditor_show' )
      print( "5" )
    except :
      print( "exception" )

