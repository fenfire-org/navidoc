# 
# Copyright (c) 2003 by Asko Soukka
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

# $Id: config.py,v 1.39 2003/06/30 13:56:09 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
Navidoc configuration module.
"""

dbg = None

import os, ConfigParser

import navidoc.util.debug

# General debug filter
dbg = navidoc.util.debug.DebugFilter()

# System calls
metapost = 'mpost'
pnmscale = 'pnmscale'
pstopnm = 'pstopnm'
pnmtopng = 'pnmtopng'
stderr = '/dev/null'

# Initializing dynamic settings
# These should be kept up-to-date in code
# always when compiling reST or diagrams
working_directory = '.'
input_filename = ''
output_filename = ''
link_base_directory = None # if different than working_directory

# Set the default docutils.conf
docutils_conf = './docutils.conf'

# Set the default navidoc.conf
navidoc_conf = './navidoc.conf'
read_navidoc_conf = ''

# Holder of packagenames when linking diagrams
# will be cleaned after every diagram
linkpackages = {}

# Should linked parts of the diagram be emphasized
# using colors and rough edge
link_emphasize = 0

# Should diagrams be generated at all
# this is altered to halt image generation
# temporarily
mp_generate = 1

# Generate only eps -versions of diagrams
# Usable, when compiling reSTs into LaTeX
mp_eps_only = 0

# Should context menu be added into diagrams
# this is modifiable later as UML direvtive option
mp_context_menu = 0

def read_config(module, filepath):
    """
    read_config(module, filepath)
    
    Reads a config file and updates
    attributes in module.
    """
    cp = ConfigParser.ConfigParser()
    cp.read(filepath)
    for section in cp.sections():
        for option in cp.options(section):
            setattr(module, option, eval(cp.get(section, option)))
