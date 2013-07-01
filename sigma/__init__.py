#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sigma implementation.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

import os
import sys
import re
import copy
import __builtin__
import StringIO

import info


ABOUT_TYPES = [
  { 'TYPE': 'py',
    'ANCHOR': '##',
    'EXTENSIONS': [ 'py', 'pyw' ],
    'FILENAMES': [],
    'SHEBANGS': [
      '/usr/bin/env python',
      '/usr/bin/env pythonw',
      '/usr/bin/python',
      '/usr/bin/pythonw'
    ]
  },
  { 'TYPE': 'rb',
    'ANCHOR': '##',
    'EXTENSIONS': [ 'rb', 'rbw' ],
    'FILENAMES': [],
    'SHEBANGS': [
      '/usr/bin/env ruby',
      '/usr/bin/env rubyw',
      '/usr/bin/ruby',
      '/usr/bin/rubyw'
    ]
  },
  { 'TYPE': 'cpp',
    'ANCHOR': '//',
    'EXTENSIONS': [ 'cpp', 'h' ],
    'FILENAMES': [],
    'SHEBANGS': []
  },
  { 'TYPE': 'vim',
    'ANCHOR': '""',
    'EXTENSIONS': [],
    'FILENAMES': [ '.vimrc', '_vimrc' ],
    'SHEBANGS': []
  }
]

##! A bit of functional programming.
def tap( f, * v, ** k ): return [ f.__call__( * v, ** k ), f.__self__ ][ 1 ]
def reduce_collections( acc, cur ): return tap( acc.extend, list( cur ) )
def extend( * v ): return reduce( reduce_collections, v, [] )
def startswith( p, l ): return [ s for s in l if s.startswith( p ) ]


ANCHORS = set( startswith( 'ANCHORS_', globals().keys() ) )
##! Tuple, since it compatible with |basestring.startswith()|.
ANCHORS_CODE_BEGIN = ("{ ", "{\t")
ANCHORS_CODE_END   = ("}",)
ANCHORS_MULTILINE  = ("  ", "\t")
ANCHORS_TOC        = ("@ ", )
##  List of all anchors, auto generated based on tuples above.
ANCHORS = set( startswith( 'ANCHORS_', globals().keys() ) ) - ANCHORS
ANCHORS = tuple( extend( * [ globals()[ s ] for s in ANCHORS ] ) )


def preprocessFile( s_filename, s_encoding = None, ** m_args ):
  with open( s_filename ) as oFile:
    sData = oFile.read()
  if s_encoding is None:
    s_encoding = tryDetectEncoding( sData )
  sType = tryDetectType( sData, s_filename, s_encoding )
  ##  Preprocess file text, call python code.
  sNewData = preprocess( sData.decode( s_encoding ), sType, ** m_args )
  ##  Write back changed text.
  oFile = open( s_filename, "w+" )
  oFile.write( sNewData.encode( s_encoding ) )
  oFile.close()


def parseFile( s_filename, s_encoding = None, ** m_args ):
  with open( s_filename ) as oFile:
    sData = oFile.read()
  if s_encoding is None:
    s_encoding = tryDetectEncoding( sData )
  sType = tryDetectType( sData, s_filename, s_encoding )
  return parse( sData.decode( s_encoding ), sType, ** m_args )


def preprocess( s_text, s_type = None, u_baton = None, ** m_args ):
  lOut = []
  for oTag in parse( s_text, s_type ):
    if oTag.isCode():
      lOut += oTag.rawLinesPrefix()
      lCode = oTag.codeLines()
      for sName, uVal in m_args.items():
        ##! This allows to pass context from script calling Sigma back
        ##  to script functions called by Sigma.
        lCode.insert( 0, "{0}.baton = u_baton".format( sName ) )
        ##! This allows code executed by sigma to call methods from code
        ##  importing this module.
        if hasattr( __builtin__, sName ):
          raise Exception( "\"{0}\" already in globals".format( sName ) )
        setattr( __builtin__, sName, uVal )
      sys.stdout = StringIO.StringIO()
      ##! Also save |stderr| so running script can't do strange things
      ##  like redirect it to stdout that will persist after its termination.
      sys.stderr = StringIO.StringIO()
      try:
        exec "\n".join( lCode ) in dict( globals(), u_baton = u_baton )
      finally:
        for sName, uVal in m_args.items():
          delattr( __builtin__, sName )
      sOutput = sys.stdout.getvalue()
      sys.stdout = sys.__stdout__
      sys.stderr = sys.__stderr__
      for sOutputLine in sOutput.split( "\n" ):
        ##  Append only non-empty lines.
        if sOutputLine:
          lOut.append( sOutputLine )
      lOut += oTag.rawLinesPostfix()
    else:
      lOut += oTag.rawLines()
  return "\n".join( lOut )


##x Evaluates to a list of sigma tags found in file.
def parse( s_text, s_type = None ):
  oTags = TagAccumulator()
  oTags.setAnchorForType( s_type )
  for sLine in s_text.split( "\n" ):
    sCur = sLine.strip()
    ##  Need autodetect file type?
    if not oTags.anchor():
      ##  Shebang?
      ##? This must be first check in tryDetectType()
      if sCur.startswith( "#!" ):
        oTags.setAnchorForShebang( sCur )
    else:
      sAnchor = oTags.anchor()
      ##  String starts with anchor comment?
      if sCur.startswith( sAnchor ):
        ##  Remove anchor.
        sCur = sCur[ len( sAnchor ) : ]
        ##  Code block start?
        if sCur.startswith( ANCHORS_CODE_BEGIN ):
          if oTags.current().isCode():
            raise Exception( "Unterminated code block" )
          nLine = oTags.lastLine() + 1
          oTags.newCurrent( TagCode( s_anchor = sAnchor, n_line = nLine ) )
        elif sCur.startswith( ANCHORS_CODE_END ):
          if not oTags.current().isCode():
            raise Exception( "Code block without start" )
          oTags.addRawLine( sLine )
          oTags.completeCurrent()
          continue
        elif sCur.startswith( ANCHORS_TOC ):
          nLine = oTags.lastLine() + 1
          oTags.newCurrent( TagToc( s_anchor = sAnchor, n_line = nLine ) )
        elif sCur.startswith( ANCHORS_MULTILINE ): pass
        ##  Ordinary comment?
        else:
          oTags.noTagInLine()
      ##  String don't start with anchor comment,
      else:
        if oTags.current() and oTags.current().isCode():
          ##  This text is between code begin and end anchor and need to
          ##  be replaced with code output.
          continue
        ##  Ordinary text?
        else:
          oTags.noTagInLine()
    oTags.addRawLine( sLine )
  oTags.completeCurrent()
  return oTags


def tryDetectEncoding( s_data ):
  oMatch = re.search( r'-\*-\s+coding: ([^\s]+)\s+-\*-', s_data )
  if oMatch:
    ##! Match with index 1 is firt captured match.
    sEncoding = oMatch.group( 1 )
  else:
    sEncoding = 'utf-8'
  return sEncoding


def tryDetectType( s_data, s_filename, s_encoding ):
  ##  File type to detect.
  sType = None
  ##  File extension without dot or empty string.
  sExtFile = os.path.splitext( s_filename )[ 1 ][ 1 : ]
  ##  Try to detect type from filename.
  sNameOnly = os.path.basename( s_filename )
  for mType in ABOUT_TYPES:
    for sName in mType[ 'FILENAMES' ]:
      if sNameOnly == sName:
        return mType[ 'TYPE' ]
  ##  Try to detect type from extension.
  if sType is None:
    for mType in ABOUT_TYPES:
      for sExt in mType[ 'EXTENSIONS' ]:
        if sExt == sExtFile:
          return mType[ 'TYPE' ]
  return None


class TagAccumulator( list ):


  def __init__( self ):
    list.__init__( self )
    self._tagCur_o = None
    self._anchor_s = None
    ##  1-based line number.
    self._lastLine_n = 0


  def setAnchor( self, s_anchor ):
    self._anchor_s = s_anchor


  def anchor( self ):
    return self._anchor_s


  def lastLine( self ):
    return self._lastLine_n


  def setAnchorForType( self, s_type ):
    for mType in ABOUT_TYPES:
      if mType[ 'TYPE' ] == s_type:
        self._anchor_s = mType[ 'ANCHOR' ]
        return


  def setAnchorForShebang( self, s_shebang ):
    s_shebang = s_shebang[ len( "#!" ) : ]
    for mType in ABOUT_TYPES:
      for sShebang in mType[ 'SHEBANGS' ]:
        if s_shebang.startswith( sShebang ):
          self._anchor_s = mType[ 'ANCHOR' ]
          return


  def newCurrent( self, o_tag ):
    if self._tagCur_o is not None:
      self.append( self._tagCur_o )
    self._tagCur_o = o_tag


  def current( self ):
    return self._tagCur_o


  def addRawLine( self, s_line ):
    self._lastLine_n += 1
    if self._tagCur_o is None:
      nLine = self._lastLine_n
      self._tagCur_o = TagTxt( s_anchor = self._anchor_s, n_line = nLine )
    self._tagCur_o.addRawLine( s_line )


  def completeCurrent( self ):
    self.newCurrent( None )


  ##x Line contains no sigma tag - if some non-text tag is set as current -
  ##  add it to list.
  def noTagInLine( self ):
    if self._tagCur_o is not None and not self._tagCur_o.isTxt():
      self.append( self._tagCur_o )
      self._tagCur_o = None


class Tag( object ):


  def __init__( self, s_anchor, n_line = None, l_raw = [] ):
    ##  1-based line number of tag start.
    self._line_n = n_line
    self._val_s = ""
    self._anchor_s = s_anchor
    self._raw_l = []
    for s in l_raw:
      self.addRawLine( s )


  def isTxt( self ): return False


  def isCode( self ): return False


  def isToc( self ): return False


  def isUnknown( self ): return False


  def value( self ):
    return self._val_s


  def anchor( self ):
    return self._anchor_s


  def line( self ):
    return self._line_n


  def addRawLine( self, s_line ):
    self._raw_l.append( s_line )
    sLine = s_line.strip()
    ##  Starts with anchor like '##'?
    if self.anchor() and s_line.startswith( self.anchor() ):
      sLine = sLine[ len( self.anchor() ): ]
      for sAnchor in ANCHORS:
        ##  Starts with any anchor?
        if sLine.startswith( sAnchor ):
          if len( self._val_s ) > 0:
            self._val_s += "\n"
          ##  Add text without left (anchor) part into 'value' - this can be
          ##  something sensible to formatting like Python code or some
          ##  markup language like Xi, so spaces before text are important.
          self._val_s += sLine[ len( sAnchor ) : ]
      ##! Don't add line that starts with anchor (like '##') but
      ##  is not continued with known anchor (like '{ ' or '{\t') -
      ##  this is not Sigma, just some code whose comment looks like
      ##  anchor comment.


  def rawLines( self ):
    return self._raw_l


  def __str__( self ):
    sDescr = "Tag of type {0}. Raw lines:".format( type( self ) )
    for nIndex, sLine in enumerate( self._raw_l ):
      sDescr += "\n  {0}: \"{1}\"".format( nIndex, sLine )
    return sDescr


  def __cmp__( self, other ):
    if isinstance( other, Tag ):
      if type( self ) == type( other ) and self._raw_l == other._raw_l:
        return 0
      return 1
    assert False


class TagTxt( Tag ):


  def isTxt( self ): return True


class TagCode( Tag ):


  def __init__( self, s_anchor, n_line = None, l_raw = [] ):
    Tag.__init__( self, s_anchor, l_raw )
    ##  Lines with code extracted from sigma "code" tag.
    self._codeLines_l = []
    ##  Raw lines of sigma "code" tag before generated code.
    ##  |self._codeLines_l| is extracted from this for speed.
    self._rawLinesPrefix_l = []
    ##  Raw lines of sigma "code" tag after generated code.
    self._rawLinesPostfix_l = []
    for s in l_raw:
      self.addRawLine( s )


  def isCode( self ): return True


  ##x Overloads |Tag|.
  def addRawLine( self, s_line ):
    super( TagCode, self ).addRawLine( s_line )
    sLine = s_line.strip()
    if sLine.startswith( self.anchor() ):
      sLine = sLine[ len( self.anchor() ) : ]
      gAnchors = tuple( ANCHORS_CODE_BEGIN ) + tuple( ANCHORS_MULTILINE )
      for sAnchor in gAnchors:
        if sLine.startswith( sAnchor ):
          self._rawLinesPrefix_l.append( s_line )
          self._codeLines_l.append( sLine[ len( sAnchor ) : ] )
          return
      if sLine.startswith( ANCHORS_CODE_END ):
        self._rawLinesPostfix_l.append( s_line )
        return


  def rawLinesPrefix( self ):
    return self._rawLinesPrefix_l


  def codeLines( self ):
    return self._codeLines_l


  def rawLinesPostfix( self ):
    return self._rawLinesPostfix_l


class TagToc( Tag ):


  def isToc( self ): return True


class TagUnknown( Tag ):


  def isUnknown( self ): return True


def main():
  import argparse
  oParser = argparse.ArgumentParser( description = info.DESCR )
  oParser.add_argument( 'file', help = "File to preprocess." )
  oArgs = oParser.parse_args()
  preprocessFile( oArgs.file )

