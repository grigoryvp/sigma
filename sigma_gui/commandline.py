#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import argparse

import pmq

class Commandline( pmq.Actor ) :

  def m_commandline_handle( self ) :
    oParses = argparse.ArgumentParser( description = "Sigma" )
    sHelp = "Editor to interact"
    lEditors = [ 'vim' ]
    oParses.add_argument( '-editor', help = sHelp, choices = lEditors )
    oArgs = oParses.parse_args()
    pmq.post( 'm_wndeditor_show' )

