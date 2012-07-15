#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

class Project( object ) :

  def __init__( self ) :
    self.name = None
    self.dir = None
    ##  Version Control System type: 'hg', 'git' or 'svn', same as
    ##  folder name in |dir|, ex '.hg'.
    self.vcs = None

  def __eq__( self, other ) :
    if other is None :
      return False
    return self.name == other.name and \
           self.dir == other.dir and \
           self.vcs == other.vcs

