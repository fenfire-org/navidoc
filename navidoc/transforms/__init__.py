# 
# Copyright (c) 2003 by Benja Fallenstein, Asko Soukka
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

# $Id: __init__.py,v 1.12 2003/04/28 11:11:49 humppake Exp $

#
# Written by Benja Fallenstein and Asko Soukka
#

__docformat__ = 'reStructuredText'

import os.path

# Replacing existing: Avoiding "unknown target" warnings with latex writer
# ***ugly***
import docutils.transforms.universal, docutils.nodes
class FinalCheckVisitor(docutils.transforms.universal.FinalCheckVisitor):
    def visit_citation_reference(self, node):
        if node.resolved or not node.hasattr('refname'):
            return
        refname = node['refname']
        id = self.document.nameids.get(refname)
        if id is None:
            # Instead of complaining when a reference is not included
            # (i.e., there's no '.. [gzz] bla' for a '[gzz]_'),
            # we insert the missing node, empty.

            # Note: I don't really know what I'm doing here,
            # just poking around and guessing which variables
            # contain which things...

            id = refname
            xnode = docutils.nodes.reference(refid=refname)
            #node += xnode
            self.document.ids[id] = xnode
            self.document.nameids[refname] = refname

        del node['refname']
        node['refid'] = id
        self.document.ids[id].referenced = 1
        node.resolved = 1
            
        ##    msg = self.document.reporter.error(
        ##          'Unknown target name: "%s".' % (node['refname']),
        ##          base_node=node)
        ##    msgid = self.document.set_id(msg)
        ##    prb = nodes.problematic(
        ##          node.rawsource, node.rawsource, refid=msgid)
        ##    prbid = self.document.set_id(prb)
        ##    msg.add_backref(prbid)
        ##    node.parent.replace(node, prb)
        ##else:
        ##    del node['refname']
        ##    node['refid'] = id
        ##    self.document.ids[id].referenced = 1
        ##    node.resolved = 1
docutils.transforms.universal.FinalCheckVisitor = FinalCheckVisitor

import time
from docutils import nodes, utils, languages
def generate_footer(self):
    # @@@ Text is hard-coded for now.
    # Should be made dynamic (language-dependent).
    settings = self.document.settings
    lcode = settings.language_code
    language = languages.get_language(lcode)
    if settings.generator or settings.datestamp or settings.source_link \
           or settings.source_url:
        text = []
        if settings.source_link and settings._source \
               or settings.source_url:
            if settings.source_url:
                source = settings.source_url
            else:
                source = utils.relative_path(settings._destination,
                                             settings._source)
            try: label = language.labels['viewdocumentsource']
            except KeyError: label = 'View document source'
            text.extend([
                nodes.reference('', label, refuri=source), nodes.Text('.\n')])
        if settings.datestamp:
            if settings.datestamp.strip() == 'CVS_DATE':
                datestamp = '$' \
                            +'Date:$'
                label = 'Last modified'
            elif settings.datestamp.strip() == 'CVS_VERSION':
                datestamp = '$' \
                            +'Id:$'
                label = ''
            elif settings.datestamp.strip() == 'SSI_LASTMOD':
                datestamp = ''
                label = ''
                attributes = {'format': 'html'}
                text.append(nodes.Text('Last modified: '))
                text.append(nodes.raw('', '<!--#flastmod file="%s" -->' \
                                      % (os.path.basename(settings._source)),
                                      **attributes))
            else: 
                datestamp = time.strftime(settings.datestamp, time.gmtime())
                try: label = language.labels['generatedon']
                except KeyError: label = 'Generated on'
            if len(label) > 0:
                text.append(nodes.Text(label+': ' + datestamp + '.\n'))
            else:
                text.append(nodes.Text(datestamp+'.\n'))
        if settings.generator:
            try: label = language.labels['generatedby']
            except KeyError: label = 'Generated by'
            try: label2 = language.labels['from']
            except KeyError: label2 = 'from'
            try: label3 = language.labels['source']
            except KeyError: label3 = 'source'
            text.extend([
                nodes.Text(label+' '),
                nodes.reference('', 'Docutils', refuri=
                                'http://docutils.sourceforge.net/'),
                nodes.Text(' '+label2+' '),
                nodes.reference('', 'reStructuredText', refuri='http://'
                                'docutils.sourceforge.net/rst.html'),
                nodes.Text(' '+label3+'.\n')])
        footer = nodes.footer()
        footer += nodes.paragraph('', '', *text)
        return footer
    else:
        return None
docutils.transforms.universal.Decorations.generate_footer = generate_footer
