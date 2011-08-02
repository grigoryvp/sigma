#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sigma
# Copyright 2011 Grigory Petrov
# See LICENSE for details.

import os
import sys
import re
import StringIO

ABOUT_TYPES = [
  { 'TYPE' : 'py',  'SHEBANG' : 'python', 'ANCHOR' : '##' },
  { 'TYPE' : 'pyw', 'SHEBANG' : 'python', 'ANCHOR' : '##' },
  { 'TYPE' : 'cpp', 'SHEBANG' : None,     'ANCHOR' : '//' },
  { 'TYPE' : 'h',   'SHEBANG' : None,     'ANCHOR' : '//' }
]
ANCHOR_CODE_BEGIN = "{ "
ANCHOR_CODE_END   = "}"
ANCHOR_MULTILINE  = "  "

def PreprocessFile( i_sFilename, i_sEncoding = None ) :
  oFile = open( i_sFilename )
  sData = oFile.read()
  oFile.close()
  ##  Need autodetect file encoding?
  if not i_sEncoding :
    oMatch = re.search( r'-\*-\s+coding: ([^\s]+)\s+-\*-', sData )
    if oMatch :
      ##! Match with index 1 is firt captured match.
      i_sEncoding = oMatch.group( 1 )
    else :
      i_sEncoding = 'utf-8'
  ##  File extension without dot or empty string.
  sExt = os.path.splitext( i_sFilename )[ 1 ][ 1 : ]
  sType = sExt if sExt else None
  ##  Preprocess file text, call python code.
  sData = Preprocess( sData.decode( i_sEncoding ), sType )
  ##  Write back changed text.
  oFile = open( i_sFilename, "w+" )
  oFile.write( sData.encode( i_sEncoding ) )
  oFile.close()

def Preprocess( i_sTxt, i_sType = None ) :
  sAnchor = AnchorForType( i_sType )
  lOut = []
  lCode = []
  for sLine in i_sTxt.split( "\n" ) :
    sCur = sLine.strip()
    ##  Need autodetect file type?
    if not sAnchor :
      ##  Shebang?
      if sCur.startswith( "#!" ) :
        sAnchor = AnchorForShebang( sCur )
      lOut.append( sLine )
      continue
    ##  String starts with anchor comment?
    if sCur.startswith( sAnchor ) :
      ##  Remove anchor.
      sCur = sCur[ len( sAnchor ) : ]
      ##  Code block start?
      if sCur.startswith( ANCHOR_CODE_BEGIN ) :
        if [] != lCode :
          raise Exception( "Unterminated code block" )
        lCode.append( sCur[ len( ANCHOR_CODE_BEGIN ) : ] )
      elif sCur.startswith( ANCHOR_MULTILINE ) :
        if [] != lCode :
          lCode.append( sCur[ len( ANCHOR_MULTILINE ) : ] )
      elif sCur.startswith( ANCHOR_CODE_END ) :
        sCode = "\n".join( lCode )
        lCode = []
        sys.stdout = StringIO.StringIO()
        exec sCode
        sOutput = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__
        for sOutputLine in sOutput.split( "\n" ) :
          ##  Append only non-empty lines.
          if sOutputLine :
            lOut.append( sOutputLine )
      ##  Unknown anchor?
      else :
        continue
    else :
      ##  Has some code already accumulated?
      if [] != lCode :
        ##  This text is between code begin and end anchor and need to
        ##  be replaced with code output.
        continue
    lOut.append( sLine )
  return "\n".join( lOut )

def AnchorForType( i_sType ) :
  for aType in ABOUT_TYPES :
    if aType[ 'TYPE' ] == i_sType :
      return aType[ 'ANCHOR' ]
  return None

def AnchorForShebang( i_sShebang ) :
  for aType in ABOUT_TYPES :
    if aType[ 'SHEBANG' ] == i_sShebang :
      return aType[ 'ANCHOR' ]
  return None

