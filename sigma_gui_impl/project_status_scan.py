#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq


class ProjectStatusScan( pmq.Actor ) :

  def __init__( self ) :
    pmq.Actor.__init__( self )
    self.m_lProjects = []

  def m_startup( self ) :
    pmq.post( 'm_project_status_scan', delay = 1.0 )

  def m_projects( self, i_lProjects ) :
    self.m_lProjects = i_lProjects

  def m_project_status_scan( self ) :
    pmq.post( 'm_project_status_scan', delay = 1.0 )

