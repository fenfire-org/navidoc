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

# $Id: __init__.py,v 1.6 2003/04/10 11:28:00 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

import docutils.writers

from navidoc.writers import latex2e
from docutils.writers import _writer_aliases

_writer_modules = {}
_writer_aliases['latex'] = 'latex2e'
_writer_aliases['html'] = 'xhtml11'
_writer_modules['latex2e'] = 'navidoc.writers'
_writer_modules['xhtml11'] = 'navidoc.writers'

# Replacing existing: Allows writers from different modules
def get_writer_class(writer_name):
    """Return the Writer class from the `writer_name` module."""
    writer_name = writer_name.lower()
    if _writer_aliases.has_key(writer_name):
        writer_name = _writer_aliases[writer_name]
    if _writer_modules.has_key(writer_name):
        writer_module = _writer_modules[writer_name]
    else: writer_module = 'docutils.writers'
    module = __import__(writer_module, globals(), locals(), [writer_name])
    module = getattr(module, writer_name)
    return module.Writer

docutils.writers.get_writer_class = get_writer_class
