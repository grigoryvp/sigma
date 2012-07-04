#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq
import sigma

class CmdToc( pmq.Actor ) :

  def m_cmd_toc( self, i_sFile ) :
    lTags = [ o for o in sigma.parseFile( i_sFile ) if o.isToc() ]
    pmq.post( 'm_toc', lTags )

