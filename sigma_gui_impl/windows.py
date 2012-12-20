#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

import pmq

##c Handles interactions between app windows - for example, on
##  'settings' command this object will display 'settings' window.
class Windows( pmq.Actor ) :

  def m_on_settings( self ) :
    pmq.post( 'm_wndsettings_show' )

