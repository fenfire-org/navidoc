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

#$Id: docxx.py,v 1.8 2003/06/30 13:56:10 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
Doc++ link element.
"""

import config

import navidoc
import os.path, re

from navidoc.util.path import *

dbg = config.dbg.shorthand('link')
dbg_navidoc = config.dbg.shorthand('navidoc')
config.linkpackages['clink'] = ''

targets = {}

def __init__():
    global targets
    for docxx in config.docxx_directories:
        if os.path.isfile(slashify(docxx)+'index.html'):
            index = open(slashify(docxx)+'index.html')
            tuples = re.compile('<A HREF="([^<]*)">([^<]*)</A>')
            tuples = tuples.findall(index.read())
            index.close()
            for link, name in tuples:
                targets[name] = slashify(docxx)+link

class CLinkPackage(navidoc.Element):
    key = "clinkpackage"

    def __init__(self, var, toks, list):
        if len(toks) > 0: package = toks[0]
        else: package = ''
        dbg("Set clinkpackage to: "+package)
        config.linkpackages['clink'] = package

    def setup_code(self): return ''

    def draw_code(self):  return ''

class CLink(navidoc.link.Link):
    key = "clink"

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
                dbg_navidoc('[clink] Target not found: %s.' % (self.target))
            dbg(self.key+" Doc++ target: %s, error: %s" % (self.target, self.error))

    def set_target(self):
         """
         Set the doc++ target.
         """
         parts = self.target.split('.')
         self.target = '::'.join(parts);
         
         if targets.has_key(self.target):
             self.target = targets[self.target]
             return
         
         if len(config.linkpackages['clink']) > 0:
             package_parts = config.linkpackages['clink'].split('.')
             clinkpackage = '::'.join(package_parts)
             self.target = clinkpackage+'::'+self.target

         if targets.has_key(self.target):
             self.target = targets[self.target]
             return
         
