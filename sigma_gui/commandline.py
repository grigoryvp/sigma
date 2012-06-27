#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import argparse

import pmq

class Commandline( pmq.Actor ) :

  def m_commandline_handle( self ) :
    pmq.post( 'm_wndeditor_show' )

