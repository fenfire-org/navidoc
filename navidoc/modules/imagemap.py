#
# Copyright (c) 2003 by Asko Soukka
# 
# This file is part of Navidoc.
# 
# Navidoc is free softSware; you can redistribute it and/or modify it under
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

#$Id: imagemap.py,v 1.14 2003/08/11 10:44:55 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
The postprocessing module, which creates imagemaps
for linked diagrams and embeds focused and imagemapped
diagrams also into target documents.
"""

import config

import os.path, re

from navidoc.mp import create_uml, MPLink, psbbox

from navidoc.util.path import *

dbg = config.dbg.shorthand('imagemap')
dbg_navidoc = config.dbg.shorthand('navidoc')

def postprocess(path):
    """
    HTML postprocessing function called from rst2any.py.
    """

    dirlist = []
    if (os.path.isfile(path)): embed_imagemap(path)
    else: dirlist = listdir(path, "html", dirs=1)

    for entry in dirlist:        
        if os.path.isdir(slashify(path)+entry) \
               and not os.path.islink(slashify(path)+entry):
            postprocess(slashify(path)+entry)
        elif os.path.isfile(slashify(path)+entry):
            embed_imagemap(slashify(path)+entry)

def embed_javascript(filepath):
    html_file = open(filepath)
    html = html_file.read()
    html_file.close()

    if html.find('function setImg') == -1:
        insert = html.upper().find('</HEAD>')
        out = open(filepath, "w")            
        out.write(html[:insert]);
        out.write("""
<script language="JavaScript">
<!-- Begin JavaScript
function setImg(img_id, img_src, img_usemap) {
document[img_id].setAttribute("src", img_src);
document[img_id].setAttribute("usemap", img_usemap);
}
// End -->
</script>
""")
        out.write(html[insert:])
        out.close()

def embed_imagemap(filepath):
    dbg('Checking %s for imagemapping diagrams' % (filepath))

    config.working_directory = os.path.normpath(os.path.dirname(filepath))
    config.input_filename = os.path.basename(filepath)
    config.output_filename = os.path.basename(filepath)

    embed_javascript(filepath)
    
    htmlfile = open(filepath)
    html = htmlfile.read()
    htmlfile.close()
    
    insert = html.find('<img _uml="')
    while insert > -1:
        diagram = html[insert+11:html.find('"', insert+11)]
        
        context = filepath.replace("/","_")
        if context.endswith(config.midfix+'.html'):
            context = context[0:len(context)-(len(config.midfix)+5)]
        if context.endswith(".html"): context = context[0:len(context)-5]

        out = open(filepath, "w")            
        out.write(html[0:insert]);
        if not is_linked(diagram):
            out.write('<img')
            html = html[html.find('"', insert+11)+1:len(html)]
        else:
            out.close()
            create_uml(diagram, context)
            create_uml(diagram, context+'_implicit', scale=0.5)
            out = open(filepath, "w")            
            out.write(html[0:insert]);
            dbg_navidoc("Mapping diagram %s within %s" % (diagram, filepath))
            imgmap = get_imagemap(diagram, context)
            imgmap_implicit = get_imagemap(diagram, context+'_implicit', scale=0.5, id_postfix="_implicit")
            dbg("Diagram %s imagemap: %s" % (diagram, "\n"+str(imgmap)))
            out.write("\n"+'<a id="%s"></a>' %(diagram) + "\n")
            out.write(imgmap)
            out.write(imgmap_implicit)
            if len(context) > 0: context = '_'+context
            out.write('<img src="'+slashify(relative_path(config.working_directory, config.mp_directory)) \
                  +diagram+context+config.midfix+'.png" usemap="#' \
                  +diagram+'_map" alt="'+diagram+'" id="'+diagram+'_img" />'+"\n")
            html = html[html.find(">", insert)+1:len(html)]
        out.write(html)
        out.close()
                
        htmlfile = open(filepath)
        html = htmlfile.read()
        htmlfile.close()
        insert = html.find('<img _uml="')

        implicit_targets = get_targets(diagram)
        dbg('Diagram %s implicit targets: %s' % (diagram, str(implicit_targets)))
        for target in implicit_targets: 
            tmp = target.rfind("#")
            if tmp != -1: target = target[0:tmp]
            if os.path.isfile(target):
                embed_implicit_diagram(target, diagram) 


def embed_implicit_diagram(filepath, diagram):
    dbg_navidoc('Embedding implicitly diagram %s into %s' % (diagram, filepath))

    config.link_base_directory = config.working_directory
    init_input_filename = config.input_filename
    init_output_filename = config.output_filename
    
    config.working_directory = os.path.normpath(os.path.dirname(filepath))
    config.input_filename = os.path.basename(filepath)
    config.output_filename = os.path.basename(filepath)

    embed_javascript(filepath)

    htmlfile = open(filepath)
    html = htmlfile.read()
    htmlfile.close()

    id = html.find('<a id="'+diagram+'"></a>') + 1
    insert = html.find('<map id="'+diagram)

    """If explicit diagram found, will not insert implicit on."""
    explicit = html.find('usemap="#'+diagram+'_map"')
    if explicit == -1: explicit = html.find('_uml="'+diagram)

    if not id:
        """
        When embedding implicit diagrams, the diagram id is located
        right after <body> tag. This way it could be used better
        as anchor.
        """        
        insert_id = html.upper().find('<BODY')
        insert_id = html.upper().find('>', insert_id)+1
        out = open(filepath, "w")            
        out.write(html[:insert_id]);
        out.write('<a id="'+diagram+'"></a>'+'\n')
        out.write(html[insert_id:])
        out.close()

        htmlfile = open(filepath)
        html = htmlfile.read()
        htmlfile.close()
        
    if insert == -1 and explicit == -1:
        """
        Implicit imagemaps are embedded after the first header or after
        the <body> tag.
        """
        for index in range(6):
            insert = html.upper().find('</H%s>' % (str(index)))+5
            if insert != 4: break
        if insert == 4:
            insert = html.upper().find('<BODY')
            insert = html.upper().find('>', insert)+1
        insert_left = insert
    else: insert_left = html.find('/>', html.find('<img', insert))+2
    
    if insert != -1 and explicit == -1:
        context = filepath.replace("/","_")
        if context.endswith(config.midfix+'.html'):
            context = context[0:len(context)-(len(config.midfix)+5)]
        if context.endswith(".html"): context = context[0:len(context)-5]
        create_uml(diagram, context)
        create_uml(diagram, context+'_implicit', scale=0.5)
        out = open(filepath, "w")            
        out.write(html[0:insert]);
        out.close()
        out = open(filepath, "w")            
        out.write(html[0:insert]);
        dbg("Mapping diagram %s within %s" % (diagram, filepath))
        imgmap = get_imagemap(diagram, context)
        imgmap_implicit = get_imagemap(diagram, context+'_implicit', scale=0.5, id_postfix="_implicit")
        dbg("Diagram %s imagemap: %s" % (diagram, "\n"+str(imgmap_implicit)))
        out.write(imgmap)
        out.write(imgmap_implicit)
        if len(context) > 0: context = '_'+context
        out.write('<img src="'+slashify(relative_path(config.working_directory, config.mp_directory)) \
                  +diagram+context+'_implicit'+config.midfix+'.png" usemap="#' \
                  +diagram+'_implicit_map" alt="'+diagram+'" id="'+diagram+'_img" />'+"\n")
        html = html[insert_left:len(html)]
        out.write(html)
        out.close()

    config.working_directory = config.link_base_directory
    config.input_filename = init_input_filename
    config.output_filename = init_output_filename
    config.link_base_directory = None

def is_linked(diagram):
    log_file = open(slashify(config.mp_directory)+diagram+config.midfix+'.mp.log')
    log = log_file.read()
    log_file.close()
    log = log.replace("\n",'') # MetaPost (mpost) splits lines awkwardly in the log.
    
    # Grep all linked areas from log file.
    for link in re.findall('\"LINKRECT\((.*?)\)\"', log):
	els = link.split(',')
        if els[0] != '"bbox"': return 1

    return 0

def get_imagemap(diagram, context, scale=1.0, id_postfix=''):
    if len(context) > 0: context = '_'+context

    log_file = open(slashify(config.mp_directory)+diagram+context+config.midfix+'.mp.log')
    log = log_file.read()
    log_file.close()
    log = log.replace("\n",'') # MetaPost (mpost) splits lines awkwardly in the log.
    
    links = []
    bbox = None

    # Grep all linked areas from log file.
    for link in re.findall('\"LINKRECT\((.*?)\)\"', log):
	els = link.split(',')
        if els[0] == '"bbox"': bbox = els[2:len(els)]
        else: links.append(MPLink(els))

    imgmap = None

    if len(links) > 0:
        bbox = psbbox(bbox)
        for link in links:
            if not link.target.startswith('http://') and not link.target == '':
                link.target = relative_path(config.working_directory, link.target)
            link.map_corners(bbox.map_point)

        imgmap = "\n"+'<map id="'+diagram+id_postfix+'_map" name="'+diagram+id_postfix+'_map">'+"\n" \
                 +"\n".join([link.imgmapanchor(scale=scale, diagram=diagram, context=context) \
                             for link in links]) \
                 +'</map>'+"\n"
    return imgmap

def get_targets(diagram):
    """
    Load log file generated by MetaPost while compiling diagram,
    parse link from log file and return all gathered targets.
    """
    targets = []

    log_file = open(slashify(config.mp_directory)+diagram+config.midfix+'.mp.log')
    log = log_file.read()
    log_file.close()
    log = log.replace("\n",'') # MetaPost (mpost) splits lines awkwardly in the log.

    # Grep all linked areas from log file.
    for link in re.findall('\"LINKRECT\((.*?)\)\"', log):
	els = link.split(',')
	if els[0] != '"bbox"': targets.append(MPLink(els).target)

    return targets

