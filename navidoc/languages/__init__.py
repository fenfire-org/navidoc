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

# $Id: __init__.py,v 1.1 2003/04/10 11:28:00 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

import docutils.writers

from docutils.languages import _languages

_language_modules = {}
_language_modules['fi'] = 'navidoc.languages'

# Replacing existing: Allows writers from different modules

def get_language(language_code):
    if _languages.has_key(language_code):
        return _languages[language_code]
    if _language_modules.has_key(language_code):
        language_module = _language_modules[language_code]
    else: language_module = 'docutils.languages'
    module = __import__(language_module, globals(), locals(), [language_code])
    module = getattr(module, language_code)
    _languages[language_code] = module
    return module
docutils.languages.get_language = get_language
