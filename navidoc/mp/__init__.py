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

# $Id: __init__.py,v 1.44 2003/07/28 14:44:35 humppake Exp $

#
# Written by Tuomas Lukka, Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
Metapost module.
"""

import config

import os, os.path, re
import navidoc.link, navidoc.parser

from navidoc.util.path import *
from navidoc.util.parser import random_var

dbg = config.dbg.shorthand('mp')
dbg_navidoc = config.dbg.shorthand('navidoc')
dbg_fail = config.dbg.shorthand('mp.fail')

rough_edges = []

def link_draw_code(self):
    """
    Metapost implementation of navidoc.link.draw_code.
    """
    if config.mp_eps_only: return ''
    if not config.link_emphasize: return 'showlinksize("'+self.target+'", "'+self.title+'", ('+self.bbox+'));'
    if self.error: return 'showlinkerror("'+self.target+'", "'+self.title+'", ('+self.bbox+'));'
    if not self.focus: return 'showlink("'+self.target+'", "'+self.title+'", ('+self.bbox+'));'
    else:
        if self.rough_edge:
            navidoc.mp.rough_edges.extend([self.bbox])
            return 'showfocus("'+self.target+'", "'+self.title+'", ('+self.bbox+'));'+"\n"
        else: return 'showfocus("'+self.target+'", "'+self.title+'", ('+self.bbox+'));'
navidoc.link.Link.draw_code = link_draw_code

class MetapostElement(navidoc.NamedElement):
    def repl(self, s):
	s = s.replace("%%", self.var)
	s = s.replace("%name%", self.name)
	if "stereo" in dir(self):
	    s = s.replace("%stereo%", self.stereo or "")
	return s
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    """
	return self.repl(s)

class SimpleElement(MetapostElement):
    def __init__(self, var, toks, list):
	dbg("Simple element: %s %s %s" % (var, toks, list))
	self.var = var or toks[0]
	self.name = toks[0]
	self.do_contents(list)
        if self.link != None:
            self.link.bbox = ('bboxmeasuredpic(%s)' % (self.var))

class mptitle(MetapostElement):
    key = 'title'
    def __init__(self, var, toks, list = []):
	dbg("mptitle: %s %s %s" % (var, toks, list))
        if not var: raise UMLException('No variable given name for title (%s).' %(' '.join(toks)))
        self.var = var
        self.name = var
        self.title = ' '.join(toks)

        # Removing possible quotes
        if self.title.startswith('"') and self.title.endswith('"'):
            self.title = self.title[1:len(self.title)-1]
        
        self.do_contents(list)
        if self.link != None:
            self.link.bbox = ('bboxmeasuredpic(%s)' % (self.var))
            self.link.rough_edge = 1
    def setup_code(self):
	s = """
	    picture %%.pict;
	    %%.pict = diagramTitle("""+'"'+self.title+'"'+""");
	    picmeasurements(%%);
	    """
	return self.repl(s)
    def draw_code(self):
	s = """
	    drawmeasuredpic(%%);
	    """ 
	return self.repl(s)

class mpContextMenu(MetapostElement):
    key = 'contextmenu'
    def __init__(self, var, toks, list = []):
        config.mp_context_menu = 1
    def setup_code(self):
        return ''
    def draw_code(self):
        return ''

def context_menu(diagram):
    """ Creates the "menu" above the diagram. """

    context_menu = ''
    
    # Refers must exist.
    filepath = slashify(config.mp_directory)+diagram+config.midfix+'.refers'
    if (filepath):
        refers_file = open(filepath, "r")
        refers = refers_file.readlines()
        refers_file.close()

        # Remove white spaces, just for case
        for index in range(len(refers)):
            refers[index] = refers[index].strip()
        while refers.count(''): refers.remove('')
        
        # List through in descending order.
        refer_names = {}
        for id_inv in range(len(refers)):
            id = len(refers)-(id_inv+1)
            refers[id] = refers[id].replace("\n", '')
            
            try:
                refers_file = open(refers[id], 'r')                
                title = re.compile('<title>([^<]*)</title>')
                title = title.findall(refers_file.read())
                refers_file.close()
            except IOError:
                raise MetapostException("Referenced file %s defined in %s was not found." % (refers[id], filepath))

            strip = re.compile('[a-zA-ZåäöÅÄÖ\-\_ ]*')
            if len(title) > 0: title = strip.findall(title[0])[0]
            else: title = refers[id].split("/")[-1].split(".")[0]

            if config.link_base_directory == None:
                target = relative_path(config.working_directory, refers[id])
            else:
                target = relative_path(config.link_base_directory, refers[id])
            refer_names[id] = random_var()

            element = mptitle(refer_names[id], [title],
                              [[['link'], [target]]])
            if id == len(refers)-1:
                context_menu += "\tdraw ulcorner(bbox(currentpicture))+(0,10) -- urcorner(bbox(currentpicture))+(0,10) withpen pencircle scaled 1.5pt;\n"
                context_menu += element.setup_code()
                context_menu += "\t"+refer_names[id]+".sw = ulcorner(bbox(currentpicture))+(35,0);\n"
                context_menu += element.link.draw_code()
                context_menu += element.draw_code()
            else:
                context_menu += element.setup_code()
                context_menu += "\t"+refer_names[id]+".sw = "\
                                  +refer_names[id+1]\
                                  +".nw;\n"
                context_menu += element.link.draw_code()
                context_menu += element.draw_code()
            if id == 0:
                context_menu += "\tdraw (infontBB(\"from:\", \"Helvetica\") scaled 1.3) shifted (ulcorner(bbox(currentpicture))+(2,-13));\n"                    
    return context_menu

def create_uml(diagram, context='', scale=1.0):
    """
    """
    if not os.path.isfile(slashify(config.mp_directory)+diagram+config.midfix+'.uml'):
        raise MetapostException(slashify(config.mp_directory) \
                                +diagram+config.midfix+'.uml'+' not found')
    if not os.path.isfile(slashify(config.mp_directory)+diagram+config.midfix+'.mp'):
        raise MetapostException(slashify(config.mp_directory) \
                                +diagram+config.midfix+'.mp'+' not found')
    
    s_file = open(slashify(config.mp_directory)+diagram+config.midfix+'.uml')
    s = s_file.read()
    s_file.close()
    l = navidoc.util.parser.parse_indented(s)
    m = navidoc.parser.ElementList(l)

    draw_extra = ''

    if len(context) > 0:
        context = '_'+context
        if config.mp_context_menu: draw_extra = context_menu(diagram);
    config.mp_context_menu = 0

    dir = slashify(config.mp_directory)

    gen1 = open(dir+diagram+context+config.midfix+'.mp.2', 'w')
    gen1.write(m.setup_code()+'\n')
    gen1.close()
    gen2 = open(dir+diagram+context+config.midfix+'.mp.3', 'w')
    gen2.write(m.draw_code()+"\n")
    gen2.write(draw_extra+"\n")

    global rough_edges
    for rough_bbox in rough_edges:
        """Print stored roughEdges now, on top of everything else."""
        gen2.write('drawRoughEdge(('+rough_bbox+'), (bbox currentpicture), ('+str(scale)+'));'+"\n")
    gen2.write('showlinksize("bbox", "'+diagram+'", (bbox currentpicture));'+"\n")
    gen2.close()
    rough_edges = []

    midfix = config.midfix
    gen3 = open(dir+diagram+context+config.midfix+".mp.4", "w")
    gen3.write("""
	prologues := 1;
        """)
    for include in config.mp_includes:
        gen3.write("""
	input """+slashify(relative_path(config.mp_directory, 'navidoc/mp/'))+include)
    gen3.write("""        
	beginfig(1)
	    input %(diagram)s%(context)s%(midfix)s.mp.2
	    input %(diagram)s%(midfix)s.mp
	    input %(diagram)s%(context)s%(midfix)s.mp.3
	endfig
	end
	""" % locals())
    gen3.close()

    mp2png(diagram+context, scale)

def mp2png(diagram, scale=1.0):
    """
    """
    config.dbg.out('navidoc', 'Compiling diagram '+diagram)

    syscmd = config.metapost+' --file-line-error-style ' \
             + '--interaction nonstopmode ' \
             + diagram + config.midfix + '.mp.4 >'+config.stderr

    dbg(syscmd)
    os.system('cd '+config.mp_directory+';'+syscmd)

    if config.mp_eps_only:
        if config.midfix.startswith('.'):
            midfix = '_'+config.midfix[1:]
        else: midfix = config.midfix
        os.rename(slashify(config.mp_directory)+diagram+config.midfix+'.mp.1',
                  slashify(config.mp_directory)+diagram+midfix+'.eps')
        return

    log_file = open(slashify(config.mp_directory)+diagram+config.midfix+'.mp.log')
    log = log_file.read()
    log_file.close()
    
    if log.find("\n"+'!') != -1:
        dbg_navidoc('[mp] Converting diagram %s failed.' % (diagram))
        dbg_fail('An error was found from MetPost log when convertin diagram %s. The log is shown below.' % (diagram))
        dbg_fail(log)
    
    links = []
    log = log.replace("\n",'') # mpost splits lines awkwardly in the log.

    bbox = 0
    scaling = 2
    list = ''

    # grep all linked areas from log file
    for link in re.findall('\"LINKRECT\((.*?)\)\"', log):
        dbg(link)
	els = link.split(',')
	if els[0] == '"bbox"':
	    bbox = els
	else:
            dbg(els)
	    links.append(MPLink(els))
    dbg(bbox)

    # Scale the bounding box and prepares it for pstopnm
    if (bbox):
        bbox = psbbox(bbox[2:])
        list = bbox.pstopnm(scaling)
    dbg(bbox)

    scaling = int(scaling / scale)

    dbg("List: "+str(list))

    # XXX quick hack: '-stdout' is pnm's option and should be perhaps declared somewhere else!?
    syscmd = config.pstopnm+' -stdout '+' '.join(list)+' '+slashify(config.mp_directory)+diagram+config.midfix \
             +'.mp.1 2>'+config.stderr+' | '+config.pnmscale+" -reduce %s"%(scaling)+' 2>'+config.stderr+' | '  \
             +config.pnmtopng+' -transparent =white >'+slashify(config.mp_directory) \
             +diagram+config.midfix+'.png 2>'+config.stderr

    dbg(syscmd)
    os.system(syscmd)

class psbbox:
    """
    PostScriptBoundingBox.
    """
    def __init__(self, els):
	self.x=(int(float(els[0])), int(float(els[2])))
	self.y=(int(float(els[1])), int(float(els[3])))
	self.scale = 1 # 1 point = 1 pixel
	self.w = self.scale*(self.x[1]-self.x[0])
	self.h = self.scale*(self.y[0]-self.y[1])
    def map_point(self, x, y):
	return (self.scale * (x - self.x[0]), 
		self.h - self.scale * (y - self.y[1])); # reverse y
    def pstopnm(self, scale):
	dpi = 72.0
	return ["%s"%r for r in [ "-llx", self.x[0]/dpi, "-lly", self.y[1]/dpi,
		"-urx", self.x[1]/dpi, "-ury", self.y[0]/dpi,
		"-xsize", self.w * scale, "-ysize", self.h * scale,
		"-xborder", 0, "-yborder", 0]]

class MPLink:
    def __init__(self, elements):
        """
        Initilize MetaPost link. Parse link target, title and corners
        of linked area from elements read from MP log file.
        """
	self.target = re.match('^"(.*)"$', elements[0]).group(1)
	self.title = re.match('^"(.*)"$', elements[1]).group(1)
	self.corners = [float(element) for element in elements[2:]]
	dbg("Link init: "+self.title)

    def map_corners(self, mapper):
        """
        Map exact coordinates from corner elements using
        provided mapper.
        """
	dbg("Unmapped corners: "+str(self.corners))
	self.corners = [int(element) for element in (
	    mapper(self.corners[0], self.corners[1]) +
	    mapper(self.corners[2], self.corners[3]) 
            )]
        dbg("Mapped corners: "+str(self.corners))

    def imgmapanchor(self, scale=1.0, diagram='', context=''):
        # Adding javascript thingy, when target not defined
        if context.endswith('_implicit'):
            id_postfix = ''
            context = context[:len(context)-len('_implicit')]
        else:
            id_postfix = '_implicit'
            context = context + '_implicit'
            
        if self.target == '' and diagram and context:
            self.target = "javascript:setImg('"+diagram+"_img', '"+slashify(relative_path(config.working_directory, config.mp_directory))+diagram+context+config.midfix+".png', '#"+diagram+id_postfix+"_map')"

        if not self.target.startswith('javascript') and self.target.find('#') == -1: diagram = '#'+diagram
        else: diagram = ''

        return """<area href="%s%s" shape="rect" coords="%s" target="%s" title="%s" alt="%s" />""" \
               % (self.target, diagram,
                  ",".join(["%s"%(int(c*scale)) for c in self.corners]), '_top',
                  self.title, self.title)

class MetapostException(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return self.value

def round_down(x):
    return int(float(x) - 5)
def round_up(x):
    return int(float(x) + 5)
