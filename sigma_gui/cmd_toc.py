#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# sigma: 'table of content' command implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import pmq
import sigma


class CmdToc( pmq.Actor ):


  def m_cmd_toc( self, s_file ):
    lTags = [ o for o in sigma.parseFile( s_file ) if o.isToc() ]
    pmq.post( 'm_toc', lTags )

