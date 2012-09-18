#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

class Project( object ) :

  def __init__( self ) :
    self.name = None
    self.m_sDir = None
    ##  Version Control System type: 'hg', 'git' or 'svn', same as
    ##  folder name in |dir|, ex '.hg'.
    self.vcs = None
    ##  'yes', 'no', 'unknown' or 'error'.
    self.commited = 'unknown'

  ##@ Project directory. None or non-empty unicode path.
  @property
  def dir( self ) :
    return self.m_sDir

  @dir.setter
  def dir( self, i_sDir ) :
    assert type( i_sDir ) is unicode
    i_sDir = i_sDir.strip().rstrip( u"\\/" )
    if not i_sDir :
      self.m_sDir = None
    else :
      self.m_sDir = i_sDir

  def __eq__( self, other ) :
    if other is None :
      return False
    return self.name == other.name and \
           self.dir == other.dir and \
           self.vcs == other.vcs

