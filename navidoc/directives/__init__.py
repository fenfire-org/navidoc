# 
# Copyright (c) 2003 Asko Soukka
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

# $Id: __init__.py,v 1.9 2003/06/30 13:56:10 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
Module for installing all Navidoc specific directives for Docutils.
"""

from docutils.parsers.rst import directives

from pegboard import pegboard_directive
from latex import bibliography_directive
from mp import mp_directive, uml_directive, uml_refer_directive

align_values = ('top', 'middle', 'bottom', 'left', 'center', 'right')

def align(argument):
    return directives.choice(argument, align_values)

directives._directives['pegboard'] = pegboard_directive
directives._directives['mp'] = mp_directive
directives._directives['uml'] = uml_directive
directives._directives['uml-refer'] = uml_refer_directive
directives._directives['bibliography'] = bibliography_directive

# Some additional options and changes for latex writer
from docutils.parsers.rst.directives import images

images.image.options['height'] = directives.unchanged
images.image.options['width'] = directives.unchanged
images.image.options['label'] = directives.unchanged
images.image.options['environment'] = directives.unchanged

images.figure.options.update(images.image.options)
