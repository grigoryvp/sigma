#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: internal representation for 'project' entity.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.


class Project( object ) :


  def __init__( self ) :
    self.name = None
    self.__sDir = None
    ##  Version Control System type: 'hg', 'git' or 'svn', same as
    ##  folder name in |dir|, ex '.hg'.
    self.vcs = None
    ##  'yes', 'no', 'unknown' or 'error'.
    self.commited = 'unknown'
    ##  'yes', 'no', 'unknown' or 'error'.
    self.pushed = 'unknown'
    ##  'yes', 'no', 'unknown' or 'error'.
    self.pulled = 'unknown'


  ##@ Project directory. None or non-empty unicode path.
  @property
  def dir( self ) :
    return self.__sDir


  @dir.setter
  def dir( self, s_dir ) :
    assert type( s_dir ) is unicode
    s_dir = s_dir.strip().rstrip( u"\\/" )
    if not s_dir :
      self.__sDir = None
    else :
      self.__sDir = s_dir


  def __eq__( self, other ) :
    if other is None :
      return False
    return self.name == other.name and \
           self.dir == other.dir and \
           self.vcs == other.vcs

