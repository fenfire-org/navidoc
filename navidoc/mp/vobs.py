# 
# Copyright (c) 2002, 2003 by Tuomas Lukka
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

# $Id: vobs.py,v 1.2 2003/06/30 13:56:10 humppake Exp $

#
# Written by Tuomas Lukka
#

__docformat__ = 'reStructuredText'

import config

import re

import navidoc

dbg = config.dbg.shorthand('uml')

class mpvobtransform(navidoc.mp.uml.mpassoc):
    key = 'vobtransform'
    def __init__(self, var, toks, list):
	navidoc.mp.uml.mpassoc.__init__(self, var, toks, list)
	self.a.type = "vobtransformfrom"
	self.b.type = "vobtransformto"

class mpvobtransformsub(navidoc.mp.uml.mpassoc):
    key = 'vobtransformsub'
    def __init__(self, var, toks, list):
	navidoc.mp.uml.mpassoc.__init__(self, var, toks, list)
	self.a.type = "vobtransformfromsub"
	self.b.type = "vobtransformtosub"

class mpvobin(navidoc.mp.uml.mpassoc):
    key = 'vobin'
    def __init__(self, var, toks, list):
	navidoc.mp.uml.mpassoc.__init__(self, var, toks, list)
	self.a.type = "vobinfrom"
	self.b.type = "vobinto"

class mpvobsubmatch(navidoc.mp.uml.SimpleRelation):
    key = 'vobsubmatch'
    def draw_code(self):
	return self.pathCode() + self.repl(" vobsubmatch(%%.p); ")
