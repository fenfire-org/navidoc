# 
# Copyright (c) 2002, 2003 by Tuomas Lukka, Asko Soukka
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

#$Id: __init__.py,v 1.25 2003/06/30 13:56:10 humppake Exp $

#
# Written by Tuomas Lukka, Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
Module contain the default link elements and basic methods for
checking the existence of a target file.
"""

import config

import os.path, re

import navidoc

from navidoc.util.path import *

dbg = config.dbg.shorthand('link')

class Link (navidoc.Element):
    key = 'link'

    title = '' #None
    bbox = '' #None
    focus = 0
    rough_edge = 1
    error = 0
    target = '' #None

    def __init__(self, var, toks, list):
	dbg("link: %s %s %s" % (var, toks,list))

        self.var = var or toks[0]
        self.title = toks[0]

        if config.link_base_directory == None:
            redirection_path = config.working_directory
        else: redirection_path = config.link_base_directory

        if (len(toks) > 1):
            """
            The ``link`` may be followed by an attribute, which is
            interpreted as keyword for one of the redirections mapped
            in config.
            """
            self.title = toks[0]
            redirection = toks[-1]
            if config.link_redirection.has_key(redirection):
                toks.remove(redirection)
                redirection_path = config.link_redirection[redirection]
                dbg('Redirection %s: %s' % (redirection, redirection_path))

        if (len(list) > 0):
            """
            Multiple link could be given.
            Let the last working one overwrite others.
            """
            for link in list:
                if type(link[0]) == type([]):
                    link = link[0][0]
                else: link = link[0]
                if self.target == None or \
                       not os.path.isfile(self.target):
                    if link.startswith('http://'): self.target = link
                    else: self.target = os.path.normpath(slashify(redirection_path) + link)

            """
            Final check and setting attributes.
            """
            self.set_status(set_title=1)
        
        dbg(self.key+" title: %s, target: %s, error: %s" % (self.title, self.target, self.error))

    def set_status(self, set_title=0):
        """
        set_status(set_title=0)
        
        Check if the link target exists. Check if the target
        file is the current file. Could also parse
        <title> from the file and set it to title.
        """
        if self.target.startswith('http://'):
            self.error = 0
            return

        path = self.target

        tmp = path.rfind("#")
        if tmp != -1: path = path[0:tmp]

        if not os.path.isfile(path): self.error = 1

        if not self.error and set_title:
            file = open(path)                
            title = re.compile('<title>([^<]*)</title>')
            strip = re.compile('[a-zA-ZåäöÅÄÖ\-\_ ]*')
            title = title.findall(file.read())
            file.close()
            if len(title) > 0: self.title = strip.findall(title[0])[0]

        if not self.error and os.path.abspath(path) \
           == os.path.abspath(slashify(config.working_directory)+config.output_filename):
            self.focus = 1
            self.target = ''
            self.title = ''

        
    def setup_code(self): return ''

    def draw_code(self):
        """
        This should be overwritten by drawing implementation.
        """
        return ''
