#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq
import sigma

class CmdToc( pmq.Actor ) :

  def m_cmd_toc( self, i_sFile ) :
    with open( i_sFile ) as oFile :
      lTags = [ o for o in sigma.parse( oFile.read() ) if o.isToc() ]
      pmq.post( 'm_toc', lTags )

