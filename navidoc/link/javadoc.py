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

#$Id: javadoc.py,v 1.13 2003/08/11 11:49:19 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'


"""
Javadoc link element.
"""

import config

import navidoc
import os.path, re

from navidoc.util.path import *

dbg = config.dbg.shorthand('link')
dbg_navidoc = config.dbg.shorthand('navidoc')

config.linkpackages['jlink'] = ''

class JLinkPackage(navidoc.Element):
    key = "jlinkpackage"

    def __init__(self, var, toks, list):
        if len(toks) > 0: package = toks[0]
        else: package = ''
        dbg("Set jlinkpackage to: "+package)
        config.linkpackages['jlink'] = package

    def setup_code(self): return ''

    def draw_code(self):  return ''

class JLink(navidoc.link.Link):
    key = "jlink"

    def __init__(self, var, toks, list):
        navidoc.link.Link.__init__(self, var, toks, list)

        if not self.target or self.error:
            self.error = 0

            if len(list) > 0 and len(list[0][0][0]) > 0:
                self.target = list[0][0][0]
            else: self.target = toks[0]
            self.set_target()
            self.set_status()

            if self.error:
                dbg_navidoc('[jlink] Target not found: %s.' % (self.target))
            dbg(self.key+" Javadoc target: %s, error: %s" % (self.target, self.error))

    def _join(self, parts):
        """
        Returns a javadoc filepath constructed from given
        parts. Although, no (.html) posfix is added.
        """
        if len(parts) == 0: return ''
        for index in range(len(parts)-1):
            if parts[index][0].isupper():
                parts[index] = parts[index]+'.'
            else:
                parts[index] = parts[index]+'/'
        return ''.join(parts)

    def set_target(self):
         """
         Set the javadoc target.
         """
         parts = self.target.split('.')
         self.target = self._join(parts);

         if re.match('^[a-z]', parts[-1]):
             self.target = slashify(self.target) + 'package-summary.html'
         else:
             self.target = self.target + '.html'

         for dir in config.javadoc_directories:
             if os.path.isfile(slashify(dir)+self.target):
                 self.target = slashify(dir)+self.target
                 if self.target.endswith('/package-summary.html'):
                     self.target = self.target+'#package_description'
                 return 
 
         if len(config.linkpackages['jlink']) > 0:
             package_parts = config.linkpackages['jlink'].split('.')
             jlinkpackage = self._join(package_parts)
             self.target = slashify(jlinkpackage)+self.target

         for dir in config.javadoc_directories:
             if os.path.isfile(slashify(dir)+self.target):
                 self.target = slashify(dir)+self.target
                 if self.target.endswith('/package-summary.html'):
                     self.target = self.target+'#package_description'
                 return 

