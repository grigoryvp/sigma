#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma command-line processing.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import sys
import argparse

import pmq


class Commandline( pmq.Actor ):


  def m_start( self ):
    ##  Without command-line just display editor window.
    if 1 == len( sys.argv ) or (2 == len( sys.argv ) and '-d' in sys.argv):
      pmq.post( 'm_wndeditor_show' )
      return

    oParser = argparse.ArgumentParser( description = "Sigma" )
    sHelp = "Editor to interact"
    lEditors = [ "vim" ]
    oParser.add_argument( "-editor", help = sHelp, choices = lEditors )
    sHelp = "File to process"
    oParser.add_argument( "-file", help = sHelp )
    oSubparsers = oParser.add_subparsers( title = "Commands" )
    sHelp = "Display file table of content based on tags"
    oSubparser = oSubparsers.add_parser( "toc", help = sHelp )
    oSubparser.set_defaults( handler = self._toc )
    sHelp = "Display list of projects in workspace directory"
    oSubparser = oSubparsers.add_parser( "projects", help = sHelp )
    oSubparser.set_defaults( handler = self._projects )
    sHelp = "Display list of files in current project"
    oSubparser = oSubparsers.add_parser( "projectfiles", help = sHelp )
    oSubparser.set_defaults( handler = self._projectfiles )

    oArgs = oParser.parse_args()
    pmq.post( 'm_editor_use', oArgs.editor )
    oArgs.handler( oArgs )


  def _toc( self, o_args ):
    pmq.post( 'm_wndtoc_show' )
    pmq.post( 'm_cmd_toc', o_args.file )


  def _projects( self, o_args ):
    pmq.post( 'm_wndprojects_show' )
    pmq.post( 'm_cmd_projects' )


  def _projectfiles( self, o_args ):
    pmq.post( 'm_wndprojectfiles_show' )
    pmq.post( 'm_cmd_project_files' )

