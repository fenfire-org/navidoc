# 
# Copyright (c) 2002, 2003 Tuomas Lukka, Asko Soukka
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

# $Id: parser.py,v 1.20 2003/06/30 13:56:10 humppake Exp $

#
# Written by Tuomas Lukka, Asko Soukka
#

__docformat__ = 'reStructuredText'

import config

import mp, link

from util.parser import *

dbg = config.dbg.shorthand('parser')

class ElementFactor:
    """
    Factor to build elements imported from 'navidoc.mp' and navidoc.link'.
    """

    top_class = navidoc.Element # Elements must be inherited from the top_class

    def __init__(self, module_paths):
        self.types = {}
        # Gathers elements from modules.
        for module_path in module_paths:
            dbg ("Checking module: "+str(module_path))
            self.types.update(keys_for_classes(module_path, self.top_class))
            for module in dir(module_path):
                if module not in ['os', 're']: module = getattr(module_path, module)
                if type(module) == type(navidoc):
                    dbg ("Checking module: "+str(module))
                    # XXX Needs check for conflicting element types and raise an exception
                    self.types.update(keys_for_classes(module, self.top_class))
        dbg("Collected: "+str(self.types))

    def is_type(self, key): return self.types.has_key(key)
        
    def get_type(self, key):
        """
        get_type(key)

        Return a class reference for correct element type referred by
        the key.
        """
        if self.types.has_key(key):
            return self.types[key]
	else: raise ParserException("Unknown element key: "+key)

    def create_new(self, key, var, s, list):
        """
        create_new(key, var, s, list)

        Create and return a new element of given type. ``Var`` is name
        identifier of the new element, ``s`` parameters for it and
        ``list`` contains all its subelements.
        """
        type = self.get_type(key)
        dbg("Found element: "+str(type))
        new = type(var, s, list)
        return new

class ElementList:
    """
    Container class for parsed elements. Provide the interface
    to generate all rendering code for its elements.
    """
    def __init__(self, list):
        """
        Initializes ElementList by parsing all elements in list.
        """
        dbg("List: "+str(list))
        for key in config.linkpackages.keys():
            config.linkpackages[key] = ''
        config.element_list = self # XXX
        self.factor = ElementFactor([mp, link])
        self.list = []
        self.extras = []
        for element in list:
            element = self.parse_element(element)
            # Borders of linked elements should be drawn before element itself.
            # Move link border element from ``extras`` stack into ``elements``
            # in front of the linked element.
            if len(self.extras) > 0 and \
                   isinstance(self.extras[0], navidoc.link.Link):
                self.list.append(self.extras.pop(0))
            self.list.append(element)
        self.list.extend(self.extras)

    def add_contained_element(self, super, elements):
        """
        add_contained_element(super, elements)
        
        Add a subelement.
        """
	toks = elements[0]
        key = toks[0]
        toks.remove(key)

        # XXX Why no explicit var is given?
        if super.var != None: toks.insert(0, super.var)
        else: toks.insert(0, super.name)
        element = self.factor.create_new(key, None, toks, elements[1:])

        if isinstance(element, navidoc.link.Link):
            # mpclass may have different var and name, links should be based on name
            # and need special handling :/
            if isinstance(element, navidoc.link.Link) and super.var != super.name:
                toks[0] = super.name
                element = self.factor.create_new(key, None, toks, elements[1:])
            super.link = element
            self.extras.insert(0, element)
        else: self.extras.append(element)
            
    def parse_element(self, element):
        """
        parse_element(element)
        
        Parse a single element.
        """

	init = element[0]
        name = None

        # Catch explicit variable name from "element (foo) foo1"
        for tok in init:
            mat = re.match('^\((.*)\)$', tok)
            if mat:
                name = mat.group(1)
                init.remove(tok)

        # Catch explicit variable name from "foo = element foo1"
        if init.count('='):
            if init.index('=') != 1:
                raise ParserException('Variable preceding "=" cannot ' \
                                      +'contain any whitespaces in "%s".' % ' '.join(init))
            if len(init) < 3:
                raise ParserException('Missing element name in "%s".' % ' '.join(init))
            name = init[0]
            init = init[2:]

        dbg('Creating %s %s %s %s.' % (init[0], name, init[1:], element[1:]))
        element = self.factor.create_new(init[0], name, init[1:], element[1:])

        # element's variable name can't contain any numbers
        if hasattr(element, 'var') and element.var:
            can_s = re.subn('[0-9]', '', element.var)[0]
            if can_s != element.var: raise ParserException(
"""
Class variable name %s contains numbers.
Please, use syntax "foo = class foo123" or "class (foo) foo123"
and refer it later using "foo".'
""" % (element.var))

        if isinstance(element, navidoc.link.Link):
            element.bbox = 'bboxmeasuredpic(%s)' % (element.var)

        return element

    def setup_code(self):
	"""
        Return the code to set up the objects for user geometry code.
        """
	return "\n".join([element.setup_code() for element in self.list]) + "\n"

    def draw_code(self):
	"""
        Return code to draw the objects after the user code.
        """
	code = "\n".join([element.draw_code() for element in self.list]) + "\n"
	return code

class ParserException(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return self.value

