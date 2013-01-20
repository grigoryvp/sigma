#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sigma tests.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.


import sys
sys.dont_write_bytecode = True

import sigma


assert sigma.parse( """
#!/usr/bin/python

##{ print( "foo" )
##}
##@ This is TOC.
""".strip() ) == [
  sigma.TagTxt( s_anchor = "##", l_raw = [ "#!/usr/bin/python", "" ] ),
  sigma.TagCode( s_anchor = "##", l_raw = [ "##{ print( \"foo\" )", "##}" ] ),
  sigma.TagToc( s_anchor = "##", l_raw = [ "##@ This is TOC." ] )
]

assert sigma.parse( """
#!/usr/bin/python
##{ print( "foo" )
##}
""".strip() )[ 1 ].codeLines() == [
  "print( \"foo\" )"
]

assert sigma.parse( """
#!/usr/bin/python
##@ This is TOC.
""".strip() )[ 1 ].value() == "This is TOC."

assert sigma.parse( """
#!/usr/bin/python
##@ This is
##  multiline.
""".strip() )[ 1 ].value() == "This is\nmultiline."

assert sigma.preprocess( """
#!/usr/bin/python

##{ print( "foo" )
##}
""".strip() ) == """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip()

assert sigma.preprocess( """
#!/usr/bin/python

##{\tprint( "foo" )
##}
""".strip() ) == """
#!/usr/bin/python

##{\tprint( "foo" )
foo
##}
""".strip()

assert sigma.preprocess( """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip() ) == """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip()

assert sigma.preprocess( """
#!/usr/bin/python

##{ print( "foo" )
foo
bar
##}
""".strip() ) == """
#!/usr/bin/python

##{ print( "foo" )
foo
##}
""".strip()

assert sigma.preprocess( """
#!/usr/bin/python

##{ print( "foo" )
##\tprint( "bar" )
baz
##}
""".strip() ) == """
#!/usr/bin/python

##{ print( "foo" )
##\tprint( "bar" )
foo
bar
##}
""".strip()

assert sigma.preprocess( """
#!/usr/bin/python

##{\tprint(
##\t\t"foo"
##\t)
##}
""".strip() ) == """
#!/usr/bin/python

##{\tprint(
##\t\t"foo"
##\t)
foo
##}
""".strip()

