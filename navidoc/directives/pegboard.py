# 
# Copyright (c) 2002, 2003 by Benja Fallenstein, Vesa Kaihlavirta, Asko Soukka
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

# $Id: pegboard.py,v 1.22 2003/06/13 12:00:29 humppake Exp $

#
# Written by Benja Fallensten, Vesa Kaihlavirta, Asko Soukka
#

__docformat__ = 'reStructuredText'

import config

import os, string

from docutils import nodes
from docutils.core import Publisher

from navidoc.util.path import *

dbg = config.dbg.shorthand('pegboard')
dbg_fail = config.dbg.shorthand('pegboard.fail')

def pegcmp(a, b):
    """
    Comparison function used when sorting pegs.
    Sorts pegs primarily in descending priority order of status
    and secondarily in descending time stamp.
    """
    if config.pegboard_priorities.has_key(a['status'].capitalize().split()[0]) \
           and config.pegboard_priorities.has_key(b['status'].capitalize().split()[0]) \
           and not a['status'].lower().split() == b['status'].lower().split():
        return config.pegboard_priorities[a['status'].capitalize().split()[0]] \
               > config.pegboard_priorities[b['status'].capitalize().split()[0]] or -1
    
    as = a['last-modified'].split('-')
    bs = b['last-modified'].split('-')
    if not len(as) == 3 or not len(bs) == 3:
        return len(as) < len(bs) or (len(bs) < len(as)) * -1 or 0
    ac = int(as[0])*10000 + int(as[1])*100 + int(as[2])
    bc = int(bs[0])*10000 + int(bs[1])*100 + int(bs[2])
    return ac < bc or (ac > bc) * -1 or 0

def getTagValue(document, tagName, all=0, always_raw=0):
    """
    Returns the value of the first occurrence, or all values of all of
    the occurrences of given tagName in docutils' document tree
    """
    values = []
    if document.tagname.lower() == tagName.lower():
        if hasattr(document.children[0], 'data') and not always_raw:
            return document.children[0].data
        else:
         return document.rawsource
    if hasattr(document, 'children'):
        for child in document.children:
            value = getTagValue(child, tagName, all=all, always_raw=always_raw)
            if value and not all:
                return value
            elif value:
                if type(value) == type([]):
                    values.extend(value)
                else:
                    values.append(value)
    if len(values) > 0:
        return values
    else:
        return ''

def getFieldTagValue(document, fieldName):
    """
    Returns the value of the first occurrense of field tag with given
    field name.
    """
    if document.tagname.lower() == 'field':
        if document.children[0].rawsource.lower() == fieldName.lower():
            return document.children[1].rawsource
    if hasattr(document, 'children'):
        for child in document.children:
            value = getFieldTagValue(child, fieldName)
            if value:
                return value
    return ''

def build_pegtable():
    """
    Search all subdirs of working directory for peg files and
    parses peg metadata from them. Returns the table containing
    metadata from all the pegs.
    """

    pegtable = []

    pegdirs = [d for d in os.listdir(config.working_directory)
           if os.path.isdir(slashify(config.working_directory)+d) and d != 'CVS']

    init_working_directory = config.working_directory

    for pegdir in pegdirs:
        dbg('Processing PEG ' + pegdir)
        config.working_directory = slashify(init_working_directory)+pegdir
        
        peg = {'authors': [], 'status': config.pegboard_undefined, 'topic': pegdir,
               'stakeholders': [], 'last-modified': '', 'dir': pegdir, 'files': '',
               'html': '', 'rst': '', 'rstfiles': [], 'ignore': [] }
        
        peg['files'] = [f for f in os.listdir(config.working_directory) \
                        if os.path.isfile(slashify(config.working_directory)+f)
                        and not f.startswith('.') and '#' not in f and '~' not in f]

        if peg['files'].count('peg.rst') > 0:
            peg['rst'] = 'peg.rst'
        else:
            for pegfile in peg['files']:
                if pegfile.endswith('.rst'):
                    peg['rst'] = pegfile

        rstfiles = [f for f in peg['files'] if f.endswith('.rst')]

        config.dbg.mute('docutils')
        config.mp_generate = 0
        for rstfile in rstfiles:
            config.input_filename = rstfile
            config.output_filename = rstfile[0:len(rstfile)-4]+config.midfix+'.html'
            pub = Publisher()
            pub.set_reader('standalone', None, 'restructuredtext')
            filename = slashify(config.working_directory)+rstfile
            pub.process_command_line(argv=('--config '+config.docutils_conf+' '+filename+'').split())
            
            #conversion may fail because of bad restructuredtext
            try:
                pub.set_io()
                document = pub.reader.read(pub.source, pub.parser, pub.settings)
                pub.apply_transforms(document)
                peg['ignore'].append(config.output_filename)

                #conversion have succeeded so far, parsing peg's metadata
                #from its document tree
                if rstfile == peg['rst']:
                    peg['html'] = rstfile[0:len(rstfile)-4]+config.midfix+'.html'
                    peg['topic'] = getTagValue(document, 'title', always_raw=1)
                    peg['topic'] = peg['topic']
                    peg['last-modified'] = getFieldTagValue(document, 'last-modified')
                    #we may have got 'rawsource', which needs some tidying
                    if peg['last-modified'].startswith('$Date'):
                        peg['last-modified'] = peg['last-modified'][7:len(peg['last-modified'])-11].replace('/', '-')
                    peg['status'] = getTagValue(document, 'status') or config.pegboard_undefined
                    stakeholders = getFieldTagValue(document, 'stakeholder')
                    if not stakeholders:
                        stakeholders = getFieldTagValue(document, 'stakeholders')
                    peg['stakeholders'] = [s.strip() for s in stakeholders.split(',')]
                    peg['authors'] = getTagValue(document, 'author', all=1)
                else:
                    status = getTagValue(document, 'status')
                    if status:
                        peg['rstfiles'].append({'filename': rstfile, 'status': status})
                
            except:
                dbg_fail('PEG %s: Docutil raised an exception while converting %s. ' % (pegdir, rstfile))
                dbg_fail('Conversion failed and pegbaord data could not be collected.\n')

        config.dbg.enable('docutils')
        config.mp_generate = 1

        if not peg['html']:
            for file in peg['files']:
                if file[len(file)-5:len(file)] == '.html':
                    peg['html'] = file
                    break
                elif file[len(file)-4:len(file)] in ('.rst', '.txt'):
                    peg['html'] = file
                    break
        config.intput_filename = ''

        #finally adds peg's metadata into pegtable
        pegtable.append(peg)

    config.working_directory = init_working_directory 
    return pegtable

#create the ``.. pegboard::`` directive
def pegboard_directive(*args):

    pegtable = build_pegtable()
    pegtable.sort(pegcmp)

    # Python doesn't like this, as 'class' is reserved
    # table = nodes.table(class='pegboard')
    table = nodes.table()
    table['class'] = 'pegboard'
    tgroup = nodes.tgroup(cols=6)
    table += tgroup

    thead = nodes.thead()
    tgroup += thead
    row = nodes.row()
    thead += row

    for col in ['Status', 'Name', 'Topic', 'Authors',
                'Stakeholders', 'Files']:
        entry = nodes.entry()
        row += entry
        para = nodes.paragraph()
        entry += para
        para += nodes.Text(col)

    tbody = nodes.tbody()
    tgroup += tbody

    for peg in pegtable:
        status = peg['status'].split()

        row = nodes.row()
        if status:
            peg_class = 'peg-' + status[0].lower()
            # Python doesn't like this, as 'class' is reserved
            # row = nodes.row(class=peg_class)
            row['class'] = peg_class
            
        tbody += row

        def get_author(s):
            if config.pegboard_authors.has_key(s):
                return config.pegboard_authors[s]
            else: return s

        _authors = [get_author(s) for s in peg['authors']]
        _stakeholders = [get_author(s) for s in peg['stakeholders']]

        ref = nodes.reference(refuri=peg['dir']+'/'+peg['html'])
        text = nodes.Text(peg['dir'].split('--')[0])
        ref += text

        status_field = peg['status'].split()
        status_comment = nodes.Text(string.join(status_field[1:]))
        status_emph = nodes.emphasis()
        status_emph += status_comment
        
        status = [
            nodes.Text(status_field[0] + ' '),
            status_emph
        ]
        
        # massive uglification here because cpython doesn't like 
        # the use of the reserved word 'class'. ;-/. Gotta think of
        # something cuter.
        #row += td(status, class='peg_status_field')
        #row += td(ref, class='peg_name_field')
        #row += td(peg['topic'].split(':')[-1], class='peg_topic_field')
        #row += td(string.join(_authors, ', '), class='peg_authors_field')
        #row += td(string.join(_stakeholders, ', '), class='peg_stakeholders_field')
	temp = td(status); temp['class'] = 'peg_status_field'
        row += temp

        temp = td(ref); temp['class'] = 'peg_name_field'
        row += temp

        temp = td(peg['topic'].split(':')[-1]); temp['class'] = 'peg_topic_field'
        row += temp

        temp = td(string.join(_authors, ', ')); temp['class'] = 'peg_authors_field'
        row += temp

        temp = td(string.join(_stakeholders, ', ')); temp['class'] = 'peg_stakeholders_field'
        row += temp

        row += make_files(peg)
    
    return [table]

def td(__node, **args):
    entry = nodes.entry(**args)
    para = nodes.paragraph()
    entry += para

    if isinstance(__node, type('')) or \
           isinstance(__node, type(u'')):
        str = __node
        #mark literates
        if str.count('``')%2 == 0:
            for i in range(str.count('``')/2):
                if str.find('``') != 0:
                    para += nodes.Text(str[0:str.find('``')])
                str = str[str.find('``')+2:len(str)]
                literal = nodes.literal(para, nodes.Text(str[0:str.find('``')]))
                para += literal
                str = str[str.find('``')+2:len(str)]
        __node = nodes.Text(str)

    para += __node
    return entry

def make_files(peg):
    # again, cpython and 'class'
    # list = nodes.bullet_list(class='pain')
    list = nodes.bullet_list()
    list['class'] = 'plain'

    # entry = nodes.entry(class='peg_files_field')
    entry = nodes.entry()
    entry['class'] = 'peg_files_field'

    entry += list
    
    for file in peg['files']:
        try:
            if peg['ignore'].index(file):
                pass
        except ValueError:
            converted = 0
            status = 0
            if file != peg['rst']:
                for rstfile in peg['rstfiles']:
                    if rstfile['filename'] == file:
                        status = rstfile['status']
                for htmlfile in peg['ignore']:
                    if htmlfile == file[0:len(file)-4]+'.html':
                        converted = htmlfile
            if converted:
                href = peg['dir'] + '/' + converted

                ref = nodes.reference(anonymous=1, refuri=href)
                if status:
                    klass = 'peg-'+status.split()[0].lower()
                    #ref = nodes.reference(anonymous=1, class=klass, refuri=href)
                    ref['class'] = klass
                    
                text = nodes.Text(converted)

                ref += text
                listitem = nodes.list_item(list, ref)
                list += listitem
            else:
                href = peg['dir'] + '/' + file
                ref = nodes.reference(anonymous=1, refuri=href)
                text = nodes.Text(file)
                
                ref += text
                listitem = nodes.list_item(list, ref)
                list += listitem
    return entry

pegboard_directive.arguments = ()
pegboard_directive.options = {}
pegboard_directive.content = 0
