#!/usr/bin/env python

# 
# Copyright (c) 2002, 2003 by Asko Soukka
# 
# This file is part of Navidoc.
# 
# Navidoc is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# Navidoc is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General
# Public License along with Navidoc; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
# 

#$Id: rst2any.py,v 1.34 2003/07/22 11:03:50 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

import config
config.read_config(config, config.navidoc_conf)

import sys, os, getopt
import docutils.core

import navidoc.directives
import navidoc.writers
import navidoc.languages
import navidoc.transforms
import navidoc.modules

from navidoc.util.path import *

# Import parser "plugins" from 'navidoc/link' and 'navidoc/mp'
config.mp_includes = listdir('navidoc/mp',['mp'],dirs=0)
dirlist = listdir('navidoc/mp',['py'],dirs=0)
for module in dirlist:
    if module != '__init__.py': exec('import navidoc.mp.%s' % module[0:len(module)-3])

dirlist = listdir('navidoc/link',['py'],dirs=0)
for module in dirlist:
    if module != '__init__.py': exec('import navidoc.link.%s' % module[0:len(module)-3])

"""
The main frontend for running Navidoc.
"""

dbg = config.dbg.shorthand('navidoc')
dbg_config = config.dbg.shorthand('config')

# Docutils wants locales to be cleaned
import locale
try:
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

# Catch actions from the command line
try: sys.argv.remove('--imagemap'); imagemap = 1
except ValueError: imagemap = 0

try: sys.argv.remove('--latex'); latex = 1
except ValueError: latex = 0

try: sys.argv.remove('--html'); html = 1
except ValueError: html = 0

try: sys.argv.remove('--metalink'); metalink = 1
except ValueError: metalink = 0

try: sys.argv.remove('--navbar'); navbar = 1
except ValueError: navbar = 0

try: sys.argv.remove('--texture'); texture = 1
except ValueError: texture = 0

try: sys.argv.remove('--loop'); loop = 1
except ValueError: loop = 0

def rst2any(input):
    """
    rst2any(input)
    
    Run docutils for a single file.
    """
    last_dot = input.replace("../", "__/").rfind('.')
    if last_dot != -1: output = input[:last_dot]
    else: output = input

    dbg_config('Working directory: '+config.working_directory)
    dbg_config('Input file: '+config.input_filename)

    if (config.read_navidoc_conf != config.navidoc_conf):
        config.read_config(config, config.navidoc_conf)
        navidoc.link.docxx.__init__() # init Doc++ linking information
        # of course that could be done everytime, when processing a clink, but...
        config.read_navidoc_conf = config.navidoc_conf

    if html:
        dbg('Compiling reST '+input)
        output = output+config.midfix+'.html'
        config.output_filename = os.path.basename(output)
        dbg_config('Output file: '+config.output_filename)
        args = '--config '+config.docutils_conf+' '+input+' '+output

        config.mp_eps_only = 0
        docutils.core.publish_cmdline(writer_name='html', argv=args.split())

    if latex:
        dbg('Compiling reST '+input)
        output = output+config.midfix+'.latex'
        config.output_filename = os.path.basename(output)
        dbg_config('Output file: '+config.output_filename)
        args = '--config '+config.docutils_conf+' '+input+' '+output

        config.mp_eps_only = 1
        docutils.core.publish_cmdline(writer_name='latex', argv=args.split())

    config.output_filename = ''

def postprocess(path):
    """
    postprocess(path)
    
    Run selected postprocessing modules.
    """
    if metalink and os.path.isdir(path):
        import navidoc.modules.metalink
        config.working_directory = path
        navidoc.modules.metalink.postprocess(path)

    if navbar and os.path.isdir(path):
        import navidoc.modules.navbar
        config.working_directory = path
        navidoc.modules.navbar.postprocess(path)

    if imagemap:
        if os.path.isfile(path):
            last_dot = path.replace("../", "__/").rfind('.')
            if last_dot != -1: path = path[:last_dot]+config.midfix+'.html'
            
        config.link_emphasize = 1
        import navidoc.modules.imagemap
        config.working_directory = os.path.normpath(os.path.dirname(path))
        navidoc.modules.imagemap.postprocess(path)
        config.link_emphasize = 0

    if texture:
        if os.path.isfile(path):
            last_dot = path.replace("../", "__/").rfind('.')
            if last_dot != -1: path = path[:last_dot]+midfix+'.html'
            
        import navidoc.modules.texture
        config.working_directory = os.path.normpath(os.path.dirname(path))
        navidoc.modules.texture.postprocess(path)

def run_docutils(path):
    """
    run_docutils(path)

    Select all reST files under ``path`` directory (or the single file
    specified by ``path``) and forward them to conversion method.
    """
    if os.path.isdir(path) and not os.path.islink(path):
	dirlist = listdir(path,['rst'],dirs=1)
        if os.path.isfile(slashify(path) + 'docutils.conf'):
            config.docutils_conf = slashify(path) + 'docutils.conf'
        if os.path.isfile(slashify(path) + 'navidoc.conf'):
            config.navidoc_conf = slashify(path) + 'navidoc.conf'
        for entry in dirlist:
            run_docutils(slashify(path)+entry)

    elif os.path.isfile(path):
        config.working_directory = os.path.normpath(os.path.dirname(path))
        if os.path.isfile(slashify(config.working_directory) + 'docutils.conf'):
            config.docutils_conf = slashify(config.working_directory) + 'docutils.conf'
        if os.path.isfile(slashify(config.working_directory) + 'navidoc.conf'):
            config.navidoc_conf = slashify(config.working_directory) + 'navidoc.conf'
        config.input_filename = os.path.basename(path)
        rst2any(path)
        
    elif os.path.isfile(path+'.rst'):
        config.working_directory = os.path.normpath(os.path.dirname(path))
        if os.path.isfile(slashify(config.working_directory) + 'docutils.conf'):
            config.docutils_conf = slashify(config.working_directory) + 'docutils.conf'
        if os.path.isfile(slashify(config.working_directory) + 'navidoc.conf'):
            config.navidoc_conf = slashify(config.working_directory) + 'navidoc.conf'
        config.input_filename = os.path.basename(path+'.rst')
        rst2any(path+'.rst')
    config.input_filename = ''
    
# Catch debug parameters
dbg_names, sys.argv = getopt.getopt(sys.argv[1:], config.dbg.short, config.dbg.long)
for dbg_name in dbg_names:
    config.dbg.enable(dbg_name[1])
    print 'Enabling debug output for:', dbg_name[1]

# Conversion loop
while 1:
    
    # The first pass; Docutils with Navidoc directives
    for filepath in sys.argv:
        try: 
            run_docutils(filepath)
        except navidoc.DocutilsException, e:
            dbg("Fatal, DocutilsException: "+e.value)
            continue
        except navidoc.parser.ParserException, e:
            dbg("Fatal, ParserException: "+e.value)
            continue
        except navidoc.mp.MetapostException, e:
            dbg("Fatal, MetapostException: "+e.value)
            continue
        except navidoc.mp.uml.UMLException, e:
            dbg("Fatal, UMLException: "+e.value)
            continue

    # The second pass; Postprovessing modules
    for filepath in sys.argv:
        try:
            postprocess(filepath)
        except navidoc.DocutilsException, e:
            dbg("Fatal, DocutilsException: "+e.value)
            continue
        except navidoc.parser.ParserException, e:
            dbg("Fatal, ParserException: "+e.value)
            continue
        except navidoc.mp.MetapostException, e:
            dbg("Fatal, MetapostException: "+e.value)
            continue
        except navidoc.mp.uml.UMLException, e:
            dbg("Fatal, UMLException: "+e.value)
            continue

    if not loop: break
    print "\n\n"+'Navidoc has finished. Press Enter to recompile.'+"\n"+ \
          'Enter any other key to exit the loop and quit Navidoc.'
    if  raw_input().lower() != '':
        break
    print 'Rerunning Navidoc...'
