# 
# Copyright (c) 2002, 2003 Asko Soukka, Benja Fallenstein
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

# $Id: mp.py,v 1.12 2003/07/16 13:05:16 humppake Exp $

#
# Written by Asko Soukka, Benja Fallenstein
#

__docformat__ = 'reStructuredText'

import config

import docutils.nodes
from docutils.parsers.rst import directives

from navidoc.mp import mp2png, create_uml

from navidoc.util.path import *

dbg = config.dbg.shorthand('mp')
dbg_fail = config.dbg.shorthand('mp.fail')

def mp_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):
    """
    Metapost-directive. Write content into_path metapost sourcefile,
    add img-tag into docutils document tree and finally execute
    Metapost.
    """

    # XXX This has not been tested for while :/
    
    to_tmpdir = relative_path(config.working_directory, config.mp_directory)
    eps_only = config.mp_eps_only # Should no png files be generated

    attributes = {'name': arguments[0]}
    options['uri'] = slashify(to_tmpdir)+attributes['name']
    if not eps_only: options['uri'] += config.midfix+'.png'
    else: options['uri'] += '_gen.eps'
    options['alt'] = attributes['name']
    options['title'] = attributes['name']
    mp_node = docutils.nodes.image(block_text, **options)
    if content:
        temp = ''
        for line in content:
                temp += line + "\n"

        # XXX Quite fatal exception should be raised if a picture with
        # the same name already exists.

        mp_filename = slashify(config.mp_directory)+attributes['name']
        mp = open(mp_filename+config.midfix+'.mp.4', 'w')
        mp.write(temp)
        mp.close()

    if (config.mp_generate): mp2png(attributes['name'])
    
    return [mp_node]

mp_directive.arguments = (1, 0, 0)
mp_directive.options = {}
mp_directive.content = 1

def uml_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):
    """
    UML-directive get UML source as its content. At first the content
    is split into UML and MP parts. Then those parts are written into
    tmpdir. At last an image node "<img src=...>" is added into
    reST document tree.
    """
    
    to_tmpdir = relative_path(config.working_directory, config.mp_directory)
    eps_only = config.mp_eps_only # Should no png files be generated

    attributes = {'name': arguments[0]}
    src = slashify(to_tmpdir)+attributes['name']
    if not eps_only: src += config.midfix+'.png'
    else: src += '_gen.eps'

    options['uri'] = src
    if options.has_key('label'): options['alt'] = options['label']
    if not options.has_key('alt'): options['alt'] = "UML: "+attributes['name']
    options['_uml'] = attributes['name']
    uml_node = docutils.nodes.image(src, **options)

    # If we have a caption, we want to make this as a figure (or do we?)
    if options.has_key('caption') and len(options['caption']) > 0:
        uml_node = docutils.nodes.figure('', uml_node)
        caption = docutils.nodes.caption('', options['caption'], label=attributes['name'])
        uml_node += caption

    # Should context reference menu be embedded
    if options.has_key('menu'):
        context_menu = options['menu']
    else: context_menu = 1

    if content:
        # Split content into UML and MP parts
        files = ['', '']
        current = 0;
        temp = ''
        for line in content:
            if line.startswith('---'): # Part are separated with three or more "-"
                files[current] = temp
                current += 1
                temp = ""
            else:
                temp += line + "\n"
        files[current] = temp

        # XXX Quite fatal exception should be raised if a diagram with
        # the same name already exists.

        # Write UML and MP sourcefiles and convert them into png and html
        dir = slashify(config.mp_directory)
        diagram = attributes['name']

        uml_file = open(dir+diagram+config.midfix+'.uml', 'w')
        uml_file.write(files[0])
        if context_menu == 1: uml_file.write("\ncontextmenu\n")
        uml_file.close()
    
        mp = open(dir+diagram+config.midfix+'.mp', 'w')
        mp.write(files[1])
        mp.close()

        if (config.mp_generate): create_uml(diagram)

    add_refer(attributes['name'], 1)

    return [uml_node]

uml_directive.arguments = (1, 0, 0)
uml_directive.options = {'caption': directives.unchanged,
                         'width': directives.unchanged,
                         'alt': directives.unchanged,
                         'label': directives.unchanged,
                         'menu': directives.nonnegative_int,
                         }
uml_directive.content = 1
                
def uml_refer_directive(name, arguments, options, content, lineno,
                        content_offset, block_text, state, state_machine):
    """
    An image node "<img _uml=...>" is added into reST document tree.
    Except that diagram ``foo`` exists or is  generated later from some
    other reST-document.
    """
    
    to_tmpdir = relative_path(config.working_directory, config.mp_directory)
    eps_only = config.mp_eps_only # Should no png files be generated

    attributes = {'name': arguments[0]}
    src = slashify(to_tmpdir)+attributes['name']
    if not eps_only: src += config.midfix+'.png'
    else: src += '_gen.eps'

    uml_node =  docutils.nodes.image(_uml=attributes['name'], uri=src)
    add_refer(attributes['name'])

    return [uml_node]

uml_refer_directive.arguments = (1, 0, 0)
uml_refer_directive.options = {'caption': directives.unchanged,
                               'width': directives.unchanged,
                               'alt': directives.unchanged,
                               'label': directives.unchanged,
                               }
uml_refer_directive.content = 0

def add_refer(diagram, to_top = 0):
    """
    Add reference information for a spesific diagram. Later, context
    menus are generated from the reference information.
    """
    refer = slashify(config.working_directory)+config.output_filename
    refers_filepath = slashify(config.mp_directory)+diagram+config.midfix+".refers"
    if (os.path.isfile(refers_filepath)):
        old_refers_file = open(refers_filepath, "r")
        old_refers = old_refers_file.read()
        if old_refers.find(config.output_filename) == -1:
            if to_top:
                refers = open(refers_filepath, "w")
                refers.write(refer+"\n"+old_refers)
                refers.close()
            else:
                refers = open(refers_filepath, "a")
                refers.write(refer+"\n")
                refers.close()
        old_refers_file.close()
    else:
        refers = open(refers_filepath, "a")
        refers.write(refer+"\n")
        refers.close()
        
