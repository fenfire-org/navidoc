# 
# Copyright (c) 2003 by Asko Soukka
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

# $Id: rdf.py,v 1.1 2003/07/16 13:07:35 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

import config

import re

import navidoc

dbg = config.dbg.shorthand('rdf')

class mprdfliteral(navidoc.mp.MetapostElement):
    key = 'rdf-literal'
    def __init__(self, var, toks, list):
	dbg("rdf-resource: %s %s %s" % (var, toks, list))
        if not var and len(toks) == 1: var = toks[0]
        if not var: raise navidoc.mp.uml.UMLException('No variable name given for resource.' %(' '.join(toks)))
        self.var = var
        self.name = var
        self.title = ' '.join(toks)

        # Remove possible quotes
        if self.title.startswith('"') and self.title.endswith('"'):
            self.title = self.title[1:len(self.title)-1]

	self.do_contents(list)
        if self.link != None:
            self.link.bbox = ('bboxmeasuredpic(%s)' % (self.var))

    def setup_code(self):
	s = """
	    picture %%.titl, %%.pict;
	    %%.titl = classTitle(""" +'"'+self.title+'"'+""");
	    %%.pict = nullpicture;
	    addto %%.pict contour bbox %%.titl withcolor(1, 0.8, 0.2);
            addto %%.pict also %%.titl;
            setbounds %%.pict to bbox %%.pict;
	    picmeasurements(%%);
	    """
        
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    """
	return self.repl(s)

class mprdfresource(navidoc.mp.MetapostElement):
    key = 'rdf-resource'
    def __init__(self, var, toks, list):
	dbg("rdf-resource: %s %s %s" % (var, toks, list))
        if not var and len(toks) == 1: var = toks[0]
        if not var: raise navidoc.mp.uml.UMLException('No variable name given for resource.' %(' '.join(toks)))
        self.var = var
        self.name = var
        self.title = ' '.join(toks)

        # Remove possible quotes
        if self.title.startswith('"') and self.title.endswith('"'):
            self.title = self.title[1:len(self.title)-1]

	self.do_contents(list)
        if self.link != None:
            self.link.bbox = ('bboxmeasuredpic(%s)' % (self.var))

    def setup_code(self):
	s = """
	    picture %%.titl, %%.pict;
	    %%.titl = classTitle(""" +'"'+self.title+'"'+""");
	    %%.pict = nullpicture;
            margin := bboxmargin;
            bboxmargin := 0;
	    addto %%.pict contour (((0,1)..(1,0)..(0,-1)..(-1,0)..cycle)
                  xscaled ((xpart lrcorner bbox %%.titl - xpart llcorner bbox %%.titl)/1.6)
                  yscaled ((ypart urcorner bbox %%.titl - ypart lrcorner bbox %%.titl)/1.6)
                  shifted ((xpart lrcorner bbox %%.titl - xpart llcorner bbox %%.titl)/2,
                           (ypart urcorner bbox %%.titl - ypart lrcorner bbox %%.titl)/4)
                  withcolor (0.4, 1, 0.4));
            addto %%.pict also %%.titl;
            bboxmargin := margin;
            setbounds %%.pict to bbox %%.pict;
	    picmeasurements(%%);
	    """
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    """
	return self.repl(s)

#    def setup_code(self):
#	s = """
#	    picture %%.pict;
#	    %%.pict = classTitle("""+'"'+self.title+'"'+""");
#            picture %%.page;
#            %%.page = nullpicture;
#	    addto %%.page doublepath ((0,5)--(0,38)--(7,45)--(35,45)--(35,5)--cycle) withpen currentpen;
#	    addto %%.page doublepath ((0,38)--(7,38)--(7,45)) withpen currentpen;
#	    addto %%.page doublepath ((12,37)--(30,37)) withpen currentpen;
#	    addto %%.page doublepath ((12,32)--(30,32)) withpen currentpen;
#	    addto %%.page doublepath ((6,27)--(30,27)) withpen currentpen;
#	    addto %%.page doublepath ((6,22)--(30,22)) withpen currentpen;
#	    addto %%.page doublepath ((6,17)--(30,17)) withpen currentpen;
#	    addto %%.page doublepath ((6,12)--(30,12)) withpen currentpen;
#            addto %%.pict also %%.page shifted (center(%%.pict) + (-17, 5));
#            setbounds %%.pict to bbox %%.pict;
#	    picmeasurements(%%);
#            """
#	return self.repl(s)
#    def draw_code(self):
#	s = """
#	    drawmeasuredpic(%%);
#	    draw bboxmeasuredpic(%%);
# 	    """ 
#	return self.repl(s)
