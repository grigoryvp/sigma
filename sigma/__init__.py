#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sigma
# Copyright 2011 Grigory Petrov
# See LICENSE for details.

import os
import sys
import re
import copy
import __builtin__
import StringIO

ABOUT_TYPES = [
  { 'TYPE' : 'py',  'SHEBANG' : '/usr/bin/env python',  'ANCHOR' : '##' },
  { 'TYPE' : 'py',  'SHEBANG' : '/usr/bin/python',      'ANCHOR' : '##' },
  { 'TYPE' : 'pyw', 'SHEBANG' : '/usr/bin/env pythonw', 'ANCHOR' : '##' },
  { 'TYPE' : 'pyw', 'SHEBANG' : '/usr/bin/pythonw',     'ANCHOR' : '##' },
  { 'TYPE' : 'cpp', 'SHEBANG' : None,                   'ANCHOR' : '//' },
  { 'TYPE' : 'h',   'SHEBANG' : None,                   'ANCHOR' : '//' }
]
ANCHOR_CODE_BEGIN = "{ "
ANCHOR_CODE_END   = "}"
ANCHOR_MULTILINE  = "  "
ANCHOR_TOC        = "@ "

def preprocessFile( i_sFilename, i_sEncoding = None, ** kargs ) :
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
  sData = Preprocess( sData.decode( i_sEncoding ), sType, ** kargs )
  ##  Write back changed text.
  oFile = open( i_sFilename, "w+" )
  oFile.write( sData.encode( i_sEncoding ) )
  oFile.close()

def preprocess( i_sTxt, i_sType = None, baton = None, ** kargs ) :
  lOut = []
  for oTag in parse( i_sTxt, i_sType ) :
    if oTag.isCode() :
      lOut += oTag.rawLinesPrefix()
      lCode = oTag.codeLines()
      for sName, uVal in kargs.items() :
        ##! This allows to pass context from script calling Sigma back
        ##  to script functions called by Sigma.
        lCode.insert( 0, "{0}.baton = baton".format( sName ) )
        ##! This allows code executed by sigma to call methods from code
        ##  importing this module.
        if hasattr( __builtin__, sName ) :
          raise Exception( "\"{0}\" already in globals".format( sName ) )
        setattr( __builtin__, sName, uVal )
      sys.stdout = StringIO.StringIO()
      try :
        exec "\n".join( lCode ) in dict( globals(), baton = baton )
      finally :
        for sName, uVal in kargs.items() :
          delattr( __builtin__, sName )
      sOutput = sys.stdout.getvalue()
      sys.stdout = sys.__stdout__
      for sOutputLine in sOutput.split( "\n" ) :
        ##  Append only non-empty lines.
        if sOutputLine :
          lOut.append( sOutputLine )
      lOut += oTag.rawLinesPostfix()
    else :
      lOut += oTag.rawLines()
  return "\n".join( lOut )


##x Evaluates to a list of sigma tags found in file.
def parse( i_sTxt, i_sType = None ) :
  oTags = TagAccumulator()
  oTags.setAnchorForType( i_sType )
  for sLine in i_sTxt.split( "\n" ) :
    sCur = sLine.strip()
    ##  Need autodetect file type?
    if not oTags.anchor() :
      ##  Shebang?
      if sCur.startswith( "#!" ) :
        oTags.setAnchorForShebang( sCur )
    else :
      sAnchor = oTags.anchor()
      ##  String starts with anchor comment?
      if sCur.startswith( sAnchor ) :
        ##  Remove anchor.
        sCur = sCur[ len( sAnchor ) : ]
        ##  Code block start?
        if sCur.startswith( ANCHOR_CODE_BEGIN ) :
          if oTags.current().isCode() :
            raise Exception( "Unterminated code block" )
          oTags.newCurrent( TagCode( anchor = sAnchor ) )
        elif sCur.startswith( ANCHOR_CODE_END ) :
          if not oTags.current().isCode() :
            raise Exception( "Code block without start" )
          oTags.addRawLine( sLine )
          oTags.completeCurrent()
          continue
        elif sCur.startswith( ANCHOR_TOC ) :
          oTags.newCurrent( TagToc( anchor = sAnchor ) )
        elif sCur.startswith( ANCHOR_MULTILINE ) : pass
        ##  Unknown anchor?
        else :
          oTags.newCurrent( TagUnknown( anchor = sAnchor ) )
      else :
        if oTags.current() and oTags.current().isCode() :
          ##  This text is between code begin and end anchor and need to
          ##  be replaced with code output.
          continue
    oTags.addRawLine( sLine )
  oTags.completeCurrent()
  return oTags


class TagAccumulator( list ) :

  def __init__( self ) :
    list.__init__( self )
    self.m_oTagCur = None
    self.m_sAnchor = None

  def setAnchor( self, i_sAnchor ) :
    self.m_sAnchor = i_sAnchor

  def anchor( self ) :
    return self.m_sAnchor

  def setAnchorForType( self, i_sType ) :
    for aType in ABOUT_TYPES :
      if aType[ 'TYPE' ] == i_sType :
        self.m_sAnchor = aType[ 'ANCHOR' ]
        break

  def setAnchorForShebang( self, i_sShebang ) :
    i_sShebang = i_sShebang[ len( "#!" ) : ]
    for aType in ABOUT_TYPES :
      if aType[ 'SHEBANG' ] and i_sShebang.startswith( aType[ 'SHEBANG' ] ) :
        self.m_sAnchor = aType[ 'ANCHOR' ]
        break

  def newCurrent( self, i_oTag ) :
    if self.m_oTagCur is not None :
      self.append( self.m_oTagCur )
    self.m_oTagCur = i_oTag

  def current( self ) :
    return self.m_oTagCur

  def addRawLine( self, i_sLine ) :
    if self.m_oTagCur is None :
      self.m_oTagCur = TagTxt( anchor = self.m_sAnchor )
    self.m_oTagCur.addRawLine( i_sLine )

  def completeCurrent( self ) :
    self.newCurrent( None )


class Tag( object ) :

  def __init__( self, anchor, value = None, raw = [] ) :
    self.m_sVal = value
    self.m_sAnchor = anchor
    self.m_lRaw = raw[:]

  def isTxt( self ) : return False
  def isCode( self ) : return False
  def isToc( self ) : return False
  def isUnknown( self ) : return False

  def value( self ) :
    return self.m_sVal

  def anchor( self ) :
    return self.m_sAnchor

  def addRawLine( self, i_sLine ) :
    self.m_lRaw.append( i_sLine )

  def rawLines( self ) :
    return self.m_lRaw

  def __str__( self ) :
    sDescr = "Tag of type {0}. Raw lines:".format( type( self ) )
    for sLine in self.m_lRaw :
      sDescr += "\n  {0}".format( sLine )
    return sDescr

  def __cmp__( self, other ) :
    if isinstance( other, Tag ) :
      if type( self ) == type( other ) and self.m_lRaw == other.m_lRaw :
        return 0
      return 1
    assert False


class TagTxt( Tag ) :

  def isTxt( self ) : return True


class TagCode( Tag ) :

  def __init__( self, anchor, value = None, raw = [] ) :
    Tag.__init__( self, anchor, value, raw )
    ##  Lines with code extracted from sigma "code" tag.
    self.m_lCodeLines = []
    ##  Raw lines of sigma "code" tag before generated code.
    ##  |self.m_lCodeLines| is extracted from this for speed.
    self.m_lRawLinesPrefix = []
    ##  Raw lines of sigma "code" tag after generated code.
    self.m_lRawLinesPostfix = []

  def isCode( self ) : return True

  ##x Overloads |Tag|.
  def addRawLine( self, i_sLine ) :
    super( TagCode, self ).addRawLine( i_sLine )
    sLine = i_sLine.strip()
    if sLine.startswith( self.anchor() ) :
      sLine = sLine[ len( self.anchor() ) : ]
      for sAnchor in [ ANCHOR_CODE_BEGIN, ANCHOR_MULTILINE ] :
        if sLine.startswith( sAnchor ) :
          self.m_lRawLinesPrefix.append( i_sLine )
          self.m_lCodeLines.append( sLine[ len( sAnchor ) : ] )
          return
      if sLine.startswith( ANCHOR_CODE_END ) :
        self.m_lRawLinesPostfix.append( i_sLine )
        return

  def rawLinesPrefix( self ) :
    return self.m_lRawLinesPrefix

  def codeLines( self ) :
    return self.m_lCodeLines

  def rawLinesPostfix( self ) :
    return self.m_lRawLinesPostfix


class TagToc( Tag ) :

  def isToc( self ) : return True


class TagUnknown( Tag ) :

  def isUnknown( self ) : return True

