# 
# Copyright (c) 2003 Benja Fallenstein
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

# $Id: latex.py,v 1.5 2003/11/05 19:14:41 tjl Exp $

#
# Written by Benja Fallenstein
#

import docutils.nodes
from docutils.parsers.rst import directives

def bibliography_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):
    if options.has_key('style') and len(options['style']) > 0:
        style = options['style']
    else: style = 'abbrv'
    return [docutils.nodes.raw(
        text='\n\\bibliography{%s}\n' % (','.join(arguments)),
        format='latex')]

bibliography_directive.arguments = (1, 100, 0)
bibliography_directive.options = {'style': directives.unchanged,
                         }
bibliography_directive.content = 0
