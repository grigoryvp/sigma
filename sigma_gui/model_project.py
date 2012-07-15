#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

class Project( object ) :

  def __init__( self ) :
    self.name = None
    self.dir = None
    ##  Version Control System type: 'hg', 'git' or 'svn', same as
    ##  folder name in |dir|, ex '.hg'.
    self.vcs = None

