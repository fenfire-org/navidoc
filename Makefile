#$Id: Makefile,v 1.22 2003/08/07 11:59:20 tuukkah Exp $

all: java

clean:
	find . -name "*.pyc" | xargs rm -f
	find . -name "*.class" | xargs rm -f
	rm -rf CLASSES

TEST=.

# Use: make test TEST=test/gzz/vob/vobmatcher.test, to run a single test.
test::
	$(JYTHON) test.py $(DBG) $(TEST)

##########################################################################
# Defining variables
NAVIDOC_DEPENDS = ../depends
JVMFLAGS= -Xms64M -Xmx128M # -Xincgc
CLASSDIR=CLASSES/
CLASSPATH =$(NAVIDOC_DEPENDS)/jython.jar:$(CLASSDIR):$(shell echo $$CLASSPATH)

export CLASSPATH

ifeq (,$(JYTHONPATH))	
 JYTHONPATH=.:$(NAVIDOC_DEPENDS)/jythonlib.jar:$(NAVIDOC_DEPENDS)/pythonlib.jar:$(NAVIDOC_DEPENDS)/docutils.jar
endif

ifeq (,$(PYTHON))
 PYTHON=/usr/bin/python
endif

ifeq (,$(JYTHON))
# python.verbose can be: "error", "warning", "message", "comment", "debug"
 JYTHON=$(JAVA) $(JVMFLAGS) -Dpython.cachedir=. -Dpython.path=$(JYTHONPATH) -Dpython.verbose=message $(EDITOR_OPTION) org.python.util.jython
endif

ifeq (,$(JAVA))
 JAVA=java
endif

ifeq (,$(JAVAC))
 JAVAC=javac
endif

ifneq (,$(EDITOR))
	EDITOR_OPTION=-Duser.editor=$(EDITOR)
else
	EDITOR_OPTION=
endif

##########################################################################
# General
java:
	mkdir -p $(CLASSDIR)
	$(JAVAC) -g -d $(CLASSDIR) `find org -name '*.java'`

##########################################################################
# General documentation targets
docs: javadoc navidoc navilink

DOCPKGS= -subpackages org
#DOCPKGS= org.nongnu.navidoc.util

JAVADOCOPTS=-use -version -author -windowtitle "Navidoc Java API"
javadoc::
	find . -name '*.class' | xargs rm -f # Don't let javadoc see these
	rm -Rf doc/javadoc
	mkdir -p doc/javadoc
	javadoc $(JAVADOCOPTS) -d doc/javadoc -sourcepath . $(DOCPKGS)

peg: # Creates a new PEG, uses python for quick use
	make new-peg PEGDIR="doc/pegboard"

pegs: # Complies only pegboard
	make html RST="doc/pegboard/"
#
##########################################################################
# Navidoc targets
navidoc:: # Compiles reST into HTML
	make html RST="doc/"

navilink: # Bi-directional linking using imagemaps
	make imagemap HTML="doc/"

naviloop: # Compiles, links, loops
	make html-loop DBG="--imagemap $(DBG)" RST="$(RST)"

new-peg: # Creates a new PEG
	$(PYTHON) newpeg.py $(PEGDIR)

html: # Compiles reST into HTML, directories are processed recursively
	$(PYTHON) rst2any.py --html -d navidoc -d docutils -d pegboard -d mp.fail $(DBG) $(RST)

html-loop: # Loop version for quick recompiling
	$(PYTHON) rst2any.py --loop --html -d navidoc -d docutils -d pegboard -d mp.fail $(DBG) $(RST)

imagemap: # Bi-directional linking using imagemaps
	$(PYTHON) rst2any.py --imagemap -d navidoc -d mp.fail $(DBG) $(HTML)

latex: # Compiles reST into LaTeX, directories are processed recursively
	$(PYTHON) rst2any.py --latex -d navidoc -d docutils $(DBG) $(RST)

latex-loop: # Loop version for quick recompiling
	$(PYTHON) rst2any.py --loop --latex -d navidoc -d docutils $(DBG) $(RST)
