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

# $Id: uml.py,v 1.23 2003/07/28 14:44:35 humppake Exp $

#
# Written by Tuomas Lukka, Asko Soukka
#

__docformat__ = 'reStructuredText'

import config

import re

from navidoc.util.parser import *

dbg = config.dbg.shorthand('uml')

class UMLException(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return self.value

class mpsequence(navidoc.Element):
    key = 'sequence'
    
    def getVarForY(self, before, after):
	"""Get a variable name for a Y coordinate.
	Padding before and after.
	"""
	v1 = random_var()
	v2 = random_var()
	yvar = self.yvar
	self.ycode += """
	    numeric %(v1)s, %(v2)s;
	    %(v2)s = %(yvar)s - %(before)s - %(after)s;
	    %(v1)s = %(yvar)s - %(before)s;
	""" % locals()
	self.yvar = v2
	return v1;

    class call:
	def __init__(self, parent, sourcex, toks, list):
	    self.var = random_var()
	    self.parent = parent
	    self.targetx = "(xpart(%s.c))" % (toks[1])
	    self.targetname = toks[1]
	    if toks[1] not in parent.seqobjs:
		parent.seqobjs.append(toks[1])
	    if sourcex == None:
		# self.sourcex = "(" + self.targetx + " - 100)"
		self.sourcex = "-50"
	    else:
		self.sourcex = sourcex
	    if len(toks) > 2:
		self.text = " ".join(toks[2:])
	    else:
		self.text = "\"\""
	    self.list = parent.parse_contents(self.targetx, list)
	def setup_code(self):
	    return " ".join([el.setup_code() for el in self.list])
	def measure(self):
	    self.yu = self.parent.getVarForY(5,5)
	    for el in self.list:
		el.measure()
	    self.yl = self.parent.getVarForY(0, 15)
	def draw_code_measure(self):
	    s = """
		sequencecallmeasure(%(sourcex)s, %(targetx)s, %(yu)s, %(yl)s, %(text)s);
	    """ % self.__dict__;
	    return s + " ".join([el.draw_code_measure() for el in self.list])
	def draw_code_draw(self):
	    s = """
		sequencecall(%(sourcex)s, %(targetx)s, %(yu)s, %(yl)s, %(text)s);
	    """ % self.__dict__;
	    return s + " ".join([el.draw_code_draw() for el in self.list])

    class delete(call):
	def draw_code_measure(self):
	    s = mpsequencel.call.draw_code_measure(self)
	    self.parent.seqobjsdeletes[self.targetname] = self.yl;
	    return s

	def draw_code_draw(self):
	    s = mpsequencel.call.draw_code_draw(self)
	    return (s + 
	     " sequencedestroy( %(targetx)s, %(yl)s ); " 
		    % self.__dict__)

    class create(call):
	def measure(self):
	    self.yu = self.parent.getVarForY(10,10)
	    for el in self.list:
		el.measure()
	    self.yl = self.parent.getVarForY(20, 20)
	def draw_code_measure(self):
	    s = """
		sequencecreatemeasure(%(sourcex)s, %(targetname)s, %(yu)s, %(yl)s, %(text)s);
	    """ % self.__dict__;
	    return s + " ".join([el.draw_code_measure() for el in self.list])

	def draw_code_draw(self):
	    s = """
		sequencecreate(%(sourcex)s, %(targetname)s, %(yu)s, %(yl)s, %(text)s);
	    """ % self.__dict__;
	    return s + " ".join([el.draw_code_draw() for el in self.list])

    def __init__(self, var, toks, list):
        dbg("mpsequence: %s %s %s" % (var, toks, list))
	self.seqobjs = []
	self.seqobjsdeletes = {}
	s = toks[0]
	self.var = var or s
	self.name = s
	self.list = self.parse_contents(None, list)
	self.ycode = ""

    def parse_contents(self, source_name, list):
	l = []
	for el in list:
	    toks = el[0]
	    s = toks[0]
	    if s == "call":
		l.append(self.call(self, source_name, toks, el[1:]))
	    elif s == "delete":
		l.append(self.delete(self, source_name, toks, el[1:]))
	    elif s == "create":
		l.append(self.create(self, source_name, toks, el[1:]))
	    elif s == "return":
		pass
	    else:
		raise UMLException("Must have call or return, not '"+s+"'")
	return l
    def setup_code(self):
	return self.repl(
	    " ".join([el.setup_code() for el in self.list])
	    )
    def lifeend(self, obj):
	return self.seqobjsdeletes.get(obj, self.yvar)
    def draw_code(self):
	self.yvar = random_var()
	self.ycode = "numeric %(yvar)s; %(yvar)s = -50;" % self.__dict__;
	for el in self.list:
	    el.measure()
	m = self.ycode
	m += " ".join([el.draw_code_measure() for el in self.list])
	m += " ".join([
	    "sequencedrawlifeline(%s, %s);" % (seqobj, self.lifeend(seqobj))
            for seqobj in self.seqobjs
            ])
	m += " ".join([el.draw_code_draw() for el in self.list])
	return self.repl(m)
    def repl(self, s):
	s = s.replace("%%", self.var)
	return s

class mpclass(navidoc.mp.MetapostElement):
    key = 'class'
    def __init__(self, var, toks, list):
	dbg("mpclass: %s %s %s" % (var, toks, list))
	self.var = var or toks[0]
	self.name = toks[0]

	self.stereo = None
	for tok in toks:
	    mat = re.match('^"(.*)"$', tok)
	    if mat: self.stereo = mat.group(1)

	self.methods = self.fields = []
	self.do_contents(list)
        if self.link:
            self.link.bbox = ('bboxmeasuredpic(%s)' %(self.var))             
    def handle_contained(self, el):
	if el[0][0] == "fields":
	    self.methods = el[1:]
	elif el[0][0] == "methods":
	    self.fields = el[1:]
	else:
	    navidoc.mp.MetapostElement.handle_contained(self, el)
    def setup_code(self):
	s = """
	    picture %%.cls, %%.pict, %%.meth, %%.sep, %%.fiel, %%.stereo;
	    numeric %%.maxwid;
	    %%.cls = classTitle("%name%");
	    %%.meth = stackStrings(defaultfont, 1, METHODS);
	    %%.fiel = stackStrings(defaultfont, 1, FIELDS);
	    STEREO

	    maxwid(%%.maxwid, %%.stereo);
	    maxwid(%%.maxwid, %%.cls);
	    maxwid(%%.maxwid, %%.meth);
	    maxwid(%%.maxwid, %%.fiel);

	    maxwidctr(%%.maxwid, %%.stereo);
	    maxwidctr(%%.maxwid, %%.cls);

	    %%.sep = nullpicture;
            addto %%.sep doublepath (0,0)--(%%.maxwid,0) withpen currentpen;
            """
        if self.fields and self.methods:
            s = s + """
            %%.pict = stackpics(%%.stereo, %%.cls, %%.sep, %%.meth, %%.sep, %%.fiel);
            """
        elif self.fields or self.methods:
            s = s + """
            %%.pict = stackpics(%%.stereo, %%.cls, %%.sep, %%.meth, %%.fiel);
            """
        else:
            s = s + """
            %%.pict = stackpics(%%.stereo, %%.cls, %%.meth, %%.fiel);
            """
        s = s + """
            setbounds %%.pict to bbox %%.pict;
	    picmeasurements(%%);
	    """
	s = s.replace("FIELDS", ", ".join(
	    [ '"'+' '.join(m[0])+'"' for m in self.fields ] ))
	s = s.replace("METHODS", ", ".join(
	    [ '"'+' '.join(m[0])+'"' for m in self.methods ] ))
	if self.stereo:
	    s = s.replace("STEREO", 
		"%%.stereo = stereotype(\"%stereo%\");")
	else:
	    s = s.replace("STEREO", 
		"%%.stereo = nullpicture;")
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    draw bboxmeasuredpic(%%);
	    """ 
	return self.repl(s)

class mppackage(navidoc.mp.MetapostElement):
    key = 'package'
    def __init__(self, var, toks, list):
	dbg("mppackage: %s %s %s" % (var, toks, list))
	self.var = var or toks[0]
	self.name = toks[0]
	self.do_contents(list)
        if self.link != None:
            self.link.bbox = ('bboxmeasuredpic(%s)' % (self.var))
    def setup_code(self):
	s = """
	    picture %%.pict;
	    %%.pict = classTitle("%name%");
            setbounds %%.pict to bbox %%.pict;
	    picmeasurements(%%);
	    """
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    draw bboxmeasuredpic(%%);
	    draw (((0,0)--(15,0)--(15,5)--(0,5)--cycle) shifted %%.nw);
	    """ 
	return self.repl(s)

# XXX underlining
class mpseqobject(navidoc.mp.SimpleElement):
    key = 'seqobject'
    def setup_code(self):
	s = """
	    picture %%.titl, %%.pict;
	    picture %%.ghost.pict;
	    %%.titl = classTitle("%name%");
	    %%.pict = %%.titl;
	    addto %%.pict doublepath bbox %%.titl;
	    %%.ghost.pict = %%.titl;
	    picmeasurements(%%);
	    picmeasurements(%%.ghost);
	    xpart(%%.c) = xpart(%%.ghost.c);
	    """
	return self.repl(s)
    def draw_code(self):
	s = """
	    if not known(ypart(%%.c)):
		ypart(%%.c) = ypart(%%.ghost.c);
	    fi
	    drawmeasuredpic(%%);
	    """
	return self.repl(s)

class mpcomponent(navidoc.mp.SimpleElement):
    key = 'component'
    def setup_code(self):
	s = """
	    picture %%.titl, %%.pict;
	    %%.titl = classTitle("%name%");
	    %%.pict = %%.titl;
	    addto %%.pict doublepath bbox %%.titl;
            setbounds %%.pict to bbox %%.pict;
	    picmeasurements(%%);
	    """
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    """
	return self.repl(s)

class mpinterface(navidoc.mp.SimpleElement):
    key = 'interface'
    def setup_code(self):
	s = """
	    picture %%.titl, %%.pict, %%.intlabel.pict;
	    %%.pict = nullpicture;
	    addto %%.pict doublepath (((0,1)..(1,0)..(0,-1)..(-1,0)..cycle) scaled 5);
	    %%.intlabel.pict = classTitle("%name%");

	    picmeasurements(%%);
	    picmeasurements(%%.intlabel);
	    """
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    if not known %%.intlabel.c:
		%%.intlabel.nw = %%.se;
	    fi
	    drawmeasuredpic(%%.intlabel);
	    """
	return self.repl(s)

class mpnary(navidoc.mp.SimpleElement):
    key = 'naryassoc'
    def setup_code(self):
	s = """
	    picture %%.pict;
	    %%.pict = naryassoc;
	    picmeasurements(%%);
	    """
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    """
	return self.repl(s)

class mpbigpackage(navidoc.mp.MetapostElement):
    key = 'bigpackage'
    def __init__(self, var, toks, list):
	dbg("mpbigpackaget: %s %s %s" % (var, toks, list))
        self.elements = []
	self.var = var or toks[0]
	self.name = toks[0]

        self.link = None

        for element in list:
            try: # try to make contained element work on it's own
                element = config.element_list.parse_element(element)
                if len(config.element_list.extras) > 0 and \
                       isinstance(config.element_list.extras[0], navidoc.link.Link):
                    config.element_list.list.append(config.element_list.extras.pop(0))
                config.element_list.list.append(element)
                if hasattr(element, 'var') and element.var:
                    self.elements.append(element.var)
            except IndexError, e: # didn't work, add it as contained (usually links)
                config.element_list.add_contained_element(self, element)

        if self.link != None:
            self.link.bbox = ('bboxmeasuredpic(%s.titl)' % (self.var))

    def setup_code(self):
        s = """
        picture %%.titl.pict;
        %%.titl.pict = classTitle("%name%");
        setbounds %%.titl.pict to bbox %%.titl.pict;

        addto %%.titl.pict doublepath (urcorner(%%.titl.pict)--lrcorner(%%.titl.pict)) withpen currentpen;
	addto %%.titl.pict doublepath (ulcorner(%%.titl.pict)--llcorner(%%.titl.pict)) withpen currentpen;
	addto %%.titl.pict doublepath (ulcorner(%%.titl.pict)--urcorner(%%.titl.pict)) withpen currentpen;

        unknownpicmeasurements(%%);
        picmeasurements(%%.titl);
	%%.titl.sw = %%.nw;
	"""
        return self.repl(s)
    def draw_code(self):
        if self.elements:
            elements_sw_x = 'xpart ' + '.sw, xpart '.join(self.elements) + '.sw'
            elements_sw_y = 'ypart ' + '.sw, ypart '.join(self.elements) + '.sw'
            elements_ne_x = 'xpart ' + '.ne, xpart '.join(self.elements) + '.ne'
            elements_ne_y = 'ypart ' + '.ne, ypart '.join(self.elements) + '.ne'
        
        s = ''
        if self.elements:
            s += """
        %%.sw = (min("""+elements_sw_x+"""), min("""+elements_sw_y+""")) - (10,10);
        %%.ne = (max("""+elements_ne_x+"""), max("""+elements_ne_y+""")) + (10,10);

            """
        s += """
        picmeasurements(%%.titl);
        %%.titl.sw = %%.nw;

        draw bboxmeasuredpic(%%);
        drawmeasuredpic(%%.titl);
        """
	return self.repl(s)

class mpqual(navidoc.mp.MetapostElement):
    key = 'qual'
    def __init__(self, var, toks, list):
	self.var = var or toks[0]
	self.name = toks[0]
	self.fields = []
	self.do_contents(list)
    def handle_contained(self, el):
	if el[0][0] == "fields":
	    self.fields = el[1:]
	else:
	    navidoc.mp.MetapostElement.handle_contained(self, el)
    def setup_code(self):
	s = """
	    picture %%.pict;
	    %%.pict = stackStrings(defaultfont, 1, FIELDS);
	    addto %%.pict doublepath bbox(%%.pict) ;
	    picmeasurements(%%);
	    """
	s = s.replace("FIELDS", ", ".join(
	    [ '"'' '+' '.join(m[0])+'"' for m in self.fields ] ))
	return self.repl(s)

class mpassoc(navidoc.mp.MetapostElement):
    key = 'assoc'
    class end(navidoc.mp.MetapostElement):
	def __init__(self, var, list):
	    self.var = var
	    self.name = ""
	    self.obj = list.pop(0)
	    self.type = ""
	    self.role = " "
	    self.multi = " "
	    while len(list) > 0:
		el = list.pop(0)
		if el == "-":
		    return
		elif el == "aggreg" or el == "compos":
		    self.type = el
		else:
		    mat = re.match("^multi\((.*)\)$", el)
		    if mat:
			self.multi = mat.group(1)
			continue
		    mat = re.match("^role\((.*)\)$", el)
		    if mat:
			self.role = mat.group(1)
			continue
		    mat = re.match("^multi\((.*)\)$", el)
		    if mat:
			self.multi = mat.group(1)
			continue
		    raise UMLException("Invalid assoc adorn "+el)
	def setup_code(self):
	    s = """
		picture %%.multi, %%.role;
		path %%.p;
		%%.multi = adornmentName("MULTI");
		%%.role = adornmentName("ROLE");
		"""
	    s = s.replace("MULTI", self.multi).replace("ROLE", self.role)
	    return self.repl(s)
	def draw_code(self):
	    s = """
		%sassoc(%%.p, %%.multi, %%.role);
		"""
	    s = self.repl(s) % self.type;
	    return s

	    
    def __init__(self, var, toks, list):
        dbg("mpassoc: %s %s %s" % (var, toks, list))
	self.var = var or random_var()
	self.name = ""

        # XXX This might not be a good idea. Anyway, the point is to allow
        # creating very simple assoc with only "assoc foo" without '-' at start.
        # as in "assoc - foo".
        if toks.count('-') == 0:
            toks.insert(1, '-')
            
	self.a = self.end(self.var+".a", toks)
	toks.reverse()
	self.b = self.end(self.var+".b", toks)

    def setup_code(self):
	s = """
	    path %%.p;
	    """ + self.a.setup_code() + self.b.setup_code() 
	return self.repl(s) 
    def draw_code(self):
	s = """
	    if not known %%.p:
		%%.p = backuppath(START, END);
		show %%.p;
	    else:
		%%.p := clipmeasuredpath(START, END, %%.p);
	    fi
	    %%.a.p = subpath(0,0.5*length(%%.p)) of %%.p;
	    %%.b.p = subpath(length(%%.p),0.5*length(%%.p)) of %%.p;
	    """ + self.a.draw_code() + self.b.draw_code() 
	return self.repl(s).replace("START", self.a.obj).replace("END", self.b.obj)

class SimpleRelation(navidoc.mp.MetapostElement):
    def __init__(self, var, toks, list):
        dbg("SimpleRelation: %s %s %s" % (var, toks, list))
	self.var = var or random_var()
	self.name = ""
        if len(toks) != 2:
            raise UMLException('Error when creating SimpleRelation (%s). len(toks) != 2.' % (' '.join(toks)))
	self.start = toks[0]
	self.end = toks[1]
    def setup_code(self):
	s = """
	    path %%.p;
	    """
	return self.repl(s) 
    def pathCode(self):
	s = """
	    if not known %%.p:
		%%.p = backuppath(START, END);
		show %%.p;
	    else:
		%%.p := clipmeasuredpath(START, END, %%.p);
	    fi
	    """
	return self.repl(s).replace("START", self.start).replace("END", self.end)

class mpsupply(SimpleRelation):
    key = 'supply'
    def draw_code(self):
	return self.pathCode() + self.repl(" draw %%.p; ")

class mpuse(SimpleRelation):
    key = 'use'
    def draw_code(self):
	return self.pathCode() + self.repl(" drawarrow %%.p dashed evenly; ")

class mprealize(SimpleRelation):
    key = 'realize'
    def draw_code(self):
	return self.pathCode() + self.repl(" realize(%%.p); ")

class mpinherit(SimpleRelation):
    key = 'inherit'
    def draw_code(self):
	return self.pathCode() + self.repl(" inherit(%%.p); ")

class mpdep(SimpleRelation):
    key = 'dep'
    def __init__(self, var, toks, list):
        if len(toks) < 3: raise UMLException("Not enough arguments for 'dep' %s." % (' '.join(toks)))
        if len(toks) > 3: raise UMLException("Too many arguments for 'dep' %s." %(' '.join(toks)))
        self.stereo = None
	for tok in toks:
	    mat = re.match('^"(.*)"$', tok)
	    if mat:
                self.stereo = mat.group(1)
                toks.remove(tok)
        if self.stereo == None: raise UMLException("Dependency role not given in %s." %(' '.join(toks)))
	SimpleRelation.__init__(self, var, toks, list)
    def draw_code(self):
	return self.pathCode() + self.repl(' dep(%%.p, "%stereo%"); ')

#All placements are done in metapost code and these are deprecated

#class placement(navidoc.mp.MetapostElement):
#    def __init__(self, var, toks, list):
#	self.var = var or random_var()
#	self.name = ""
#        (self.start, self.end, self.length) = toks
#    def draw_code(self):
#        return ""

#class above(placement):
#    key = 'above'
#    def setup_code(self):
#        return self.repl(' vertically(%s, %s, %s, %s);' %
#                         (self.length, self.var, self.start, self.end))

#class under(placement):
#    key = 'under'
#    def setup_code(self):
#        return self.repl(' vertically(%s, %s, %s, %s);' %
#                         (self.length, self.var, self.end, self.start))

#class leftOf(placement):
#    key = 'leftof'
#    def setup_code(self):
#        return self.repl(' horizontally(%s, %s, %s, %s);' %
#                         (self.length, self.var, self.start, self.end))

#class rightOf(placement):
#    key = 'rightof'
#    def setup_code(self):
#        return self.repl(' horizontally(%s, %s, %s, %s);' %
#                         (self.length, self.var, self.end, self.start))
