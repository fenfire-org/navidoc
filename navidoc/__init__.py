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

#$Id: __init__.py,v 1.14 2003/06/30 13:56:10 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

import config

import docutils.core

import util.path

# Because Docutils' own relative_path had problems with
# paths beginning with '../', we had to build our own.
# Probably we can overwrite our own by Docutils' on some day :-)
docutils.utils.relative_path = util.path.relative_path

class DocutilsException(Exception):
    def __init__(self, system_message):
        self.value = system_message.astext()
        Exception.__init__(self, self.value)
    def __str__(self):
        return self.value

def docutils_system_message(self, level, message, *children, **kwargs):
    """
    See docutils.utils.Reporter.system_message()
    This modified copy redirects Docutils system messages
    to navidoc debug.
    """
    attributes = kwargs.copy()
    category = kwargs.get('category', '')
    if kwargs.has_key('category'):
	del attributes['category']
    if kwargs.has_key('base_node'):
	source, line = docutils.utils.get_source_line(kwargs['base_node'])
	del attributes['base_node']
        if source is not None:
            attributes.setdefault('source', source)
        if line is not None:
            attributes.setdefault('line', line)
    attributes.setdefault('source', self.source)
    msg = docutils.nodes.system_message(message, level=level,
					type=self.levels[level],
					*children, **attributes)
    debug, report_level, halt_level, stream = self[category].astuple()
    if level >= report_level or debug and level == 0:
        if category:
            config.dbg.out("docutils", msg.astext(), '[%s]' % category)
        else:
            config.dbg.out("docutils", msg.astext())
    if level >= halt_level:
        raise docutils.utils.SystemMessage(msg)
    if level > 0 or debug:
       self.notify_observers(msg)
    return msg
docutils.utils.Reporter.system_message = docutils_system_message
docutils.utils.SystemMessage = DocutilsException

class Element:
    """
    The general element for all subelements.
    """

class NamedElement(Element):
    """
    Element with name and linking features.
    """
    def do_contents(self, list):
        """
        do_contents(list)

        Default implementation for element to parse and
        handle its contents.
        """
        self.link = None
	for element in list:
	    self.handle_contained(element)

    def handle_contained(self, element):
        """
        handle_contained(element)

        Default implementation for element to parse and
        handle its subelement.
        """
        config.element_list.add_contained_element(self, element)
