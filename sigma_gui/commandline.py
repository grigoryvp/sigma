#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import argparse

import pmq

class Commandline( pmq.Actor ) :

  def m_commandline_handle( self ) :
    oParser = argparse.ArgumentParser( description = "Sigma" )
    sHelp = "Editor to interact"
    lEditors = [ "vim" ]
    oParser.add_argument( "-editor", help = sHelp, choices = lEditors )
    sHelp = "File to process"
    oParser.add_argument( "-file", help = sHelp )
    oSubparsers = oParser.add_subparsers()
    sHelp = "Display file table of content based on tags"
    oSubparser = oSubparsers.add_parser( "-toc", help = sHelp )

    oArgs = oParser.parse_args()
    pmq.post( 'm_wndeditor_show' )

