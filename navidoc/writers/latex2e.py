# 
# Copyright (c) 2003 Janne Kujala, Asko Soukka, Benja Fallenstein, Vesa Kaihlavirta
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

# $Id: latex2e.py,v 1.9 2003/11/05 17:33:23 benja Exp $

#
# Modified by Janne Kujala, Asko Soukka, Benja Fallenstein, Vesa Kaihlavirta
#

"""
:Author: Engelbert Gruber (hacked by the Gzz project)
:Contact: grubert@users.sourceforge.net
:Revision: $Revision: 1.9 $
:Date: $Date: 2003/11/05 17:33:23 $
:Copyright: This module has been placed in the public domain.

LaTeX2e document tree Writer.
"""

__docformat__ = 'reStructuredText'

# convention deactivate code by two # e.g. ##.

import sys
import time
import re
import string
from types import ListType
from docutils import writers, nodes, languages

#### We diss babel, because /cite didn't work :)
## country code by a.schlock.
## partly manually converted from iso and babel stuff, dialects and some
## languages remain missing (austrian, UKEnglish, brazillian etc.)
#_ISO639_TO_BABEL = {
#    'no': 'norsk',     #XXX added by hand ( forget about nynorsk?)
#    'gd': 'scottish',  #XXX added by hand
#    'hu': 'magyar',    #XXX added by hand
#    'pt': 'portuguese',#XXX added by hand
#    'sl': 'slovenian',
#    'af': 'afrikaans',
#    'bg': 'bulgarian',
#    'br': 'breton',
#    'ca': 'catalan',
#    'cs': 'czech',
#    'cy': 'welsh',
#    'da': 'danish',

#    'de': 'ngerman',  #XXX rather than german
#    'el': 'greek',
#    'en': 'english',
#    'eo': 'esperanto',
#    'es': 'spanish',
#    'et': 'estonian',
#    'eu': 'basque',
#    'fi': 'finnish',
#    'ga': 'irish',
#    'gl': 'galician',
#    'he': 'hebrew',
#    'hr': 'croatian',
#    'hu': 'hungarian',
#    'is': 'icelandic',
#    'it': 'italian',
#    'la': 'latin',
#    'nl': 'dutch',
#    'pl': 'polish',
#    'pt': 'portuguese',
#    'ro': 'romanian',
#    'ru': 'russian',
#    'sk': 'slovak',
#    'sr': 'serbian',
#    'sv': 'swedish',
#    'tr': 'turkish',
#    'uk': 'ukrainian'
#    }

class Writer(writers.Writer):

    supported = ('latex','latex2e')
    """Formats this writer supports."""

    settings_spec = (
        'LaTeX-Specific Options',
        'The LaTeX "--output-encoding" default is "latin-1".',
        (('Specify documentclass.  Default is "article".',
          ['--documentclass'],
          {'default': 'article', }),
         ('Options to the document class. Default is "10pt".',
          ['--documentclass-options'],
          {'default': '10pt' }),       
         ('Format for footnote references: one of "superscript" or '
          '"brackets".  Default is "superscript".',
          ['--footnote-references'],
          {'choices': ['superscript', 'brackets'], 'default': 'brackets',
           'metavar': '<FORMAT>'}),
         ('Link to the stylesheet in the output LaTeX file.  This is the '
          'default.',
          ['--link-stylesheet'],
          {'dest': 'embed_stylesheet', 'action': 'store_false'}),
         ('Embed the stylesheet in the output LaTeX file.  The stylesheet '
          'file must be accessible during processing (--stylesheet-path is '
          'recommended).',
          ['--embed-stylesheet'],
          {'action': 'store_true'}),
         ('Table of contents by docutils (default) or latex. Latex(writer) supports only '
          'one ToC per document, but docutils does not write pagenumbers.',
          ['--use-latex-toc'], {'default': 0}),
         ))

    settings_default_overrides = {'output_encoding': 'latin-1'}

    output = None
    """Final translated form of `document`."""

    def translate(self):
        visitor = LaTeXTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()
        self.head_prefix = visitor.head_prefix
        self.head = visitor.head
        self.body_prefix = visitor.body_prefix
        self.body = visitor.body
        self.body_suffix = visitor.body_suffix

"""
Notes on LaTeX
--------------

* Put labels inside environments::
    \chapter[optional]{title}
    \label{lab} % optional, for cross referencing
    text for this unit ...
* unnumbered sections are not written to tableofcontents.
  a. donot print numbers::
        \renewcommand{\thesection}{}
  b. use::
        \addcontentsline{file}{sec_unit}{entry}
     file toc,lof lot
     sec_unit section, subsection , ...
     entry the line::
        \numberline text pagenumber
  X. latex does not support multiple tocs in one document.
     (might be no limitation except for docutils documentation)

* sectioning::
    \part
    \chapter (report style only) 
    \section
    \subsection
    \subsubsection
    \paragraph
    \subparagraph
    \subsubparagraph (milstd and book-form styles only) 
    \subsubsubparagraph (milstd and book-form styles only)

* documentclass options

  all notitlepage.

  article: 11pt, 12pt, twoside, twocolumn, draft, fleqn, leqno, acm
  
  report: 11pt, 12pt, twoside, twocolumn, draft, fleqn, leqno, acm
  
  letter: 11pt, 12pt, fleqn, leqno, acm
  
  book: 11pt, 12pt, twoside,twocolumn, draft, fleqn, leqno
  
* width 

  * linewidth - width of a line in the local environment
  * textwidth - the width of text on the page

  Maybe always use linewidth ?
"""    

class Babel:
    """Language specifics for LaTeX."""
    def __init__(self,lang):
        self.language = lang
        if re.search('^de',self.language):
            self.quotes = ("\"`", "\"'")
        else:    
            self.quotes = ("``", "''")
        self.quote_index = 0
        
    def next_quote(self):
        q = self.quotes[self.quote_index]
        self.quote_index = (self.quote_index+1)%2
        return q

class LaTeXTranslator(nodes.NodeVisitor):
    # When options are given to the documentclass, latex will pass them
    # to other packages, as done with babel. 
    # Dummy settings might be taken from document settings
    
    # added by gzz / Vegai
    docinfo = []

    ## For narrower things (tables, docinfos use admwidth in latex construct).
    d_class = 'article'    # document.settings.stylesheet
    d_paper = 'a4paper'
    d_margins = '2cm'
    d_stylesheet_path = 'style.tex'
    # for pdflatex some other package. pslatex

    latex_head = '\\documentclass[%s]{%s}\n'
#    latex_head = '\\documentclass{%s}\n'
#    encoding = '\\usepackage[latin1]{inputenc}\n'
    linking = '\\usepackage{hyperref}\n'
#    geometry = '\\usepackage[%s,margin=%s,nohead]{geometry}\n'
    stylesheet = '\\input{%s}\n'
    # add a generated on day , machine by user using docutils version.
    generator = '%% generator Docutils: http://docutils.sourceforge.net/\n'

    # use latex tableofcontents or let docutils do it.
    use_latex_toc = 0
    # table kind: if 0 tabularx (single page), 1 longtable
    # maybe should be decided on row count.
    use_longtable = 0
    # TODO: use mixins for different implementations.
    # list environment for option-list. else tabularx
    use_optionlist_for_option_list = 1
    # list environment for docinfo. else tabularx
    use_optionlist_for_docinfo = 0 # NOT YET IN USE

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = settings = document.settings
        self.d_class = settings.documentclass
        self.d_options = settings.documentclass_options
        self.use_latex_toc = settings.use_latex_toc
        # language: labels, bibliographic_fields, and author_separators.
        # to allow writing labes for specific languages.
        self.language = languages.get_language(settings.language_code)
        self.babel = Babel(settings.language_code)
        self.author_separator = self.language.author_separators[0]
#        if _ISO639_TO_BABEL.has_key(settings.language_code):
#            self.d_options += ',%s' % \
#                    _ISO639_TO_BABEL[settings.language_code]
        self.head_prefix = [
              self.latex_head % (self.d_options,self.d_class),
#              self.latex_head % (self.d_class),
#/cite didn't work with babel (jvk)
#              '\\usepackage{babel}\n',     # language is in documents settings.
#              '\\usepackage{shortvrb}\n',  # allows verb in footnotes.
#              self.encoding,
              # * tabularx: for docinfo, automatic width of columns, always on one page.
#              '\\usepackage{tabularx}\n',
#              '\\usepackage{longtable}\n',
              # possible other packages.
              # * fancyhdr
              # * ltxtable is a combination of tabularx and longtable (pagebreaks).
              #   but ??
              #
              # extra space between text in tables and the line above them
#              '\\setlength{\\extrarowheight}{2pt}\n',
#              '\\usepackage{amsmath}\n',   # what fore amsmath. 
              '\\usepackage{graphicx}\n',
#              '\\usepackage{multirow}\n',
#              self.linking,
#              # geometry and fonts might go into style.tex.
#              self.geometry % (self.d_paper, self.d_margins),
#              #
#              self.generator,
#              # admonition width and docinfo tablewidth
#              '\\newlength{\\admwidth}\n\\addtolength{\\admwidth}{0.9\\textwidth}\n',
#             # optionlist environment
#              '\\newcommand{\\optionlistlabel}[1]{\\bf #1 \\hfill}\n'
#              '\\newenvironment{optionlist}[1]\n',
#              '{\\begin{list}{}\n'
#              '  {\\setlength{\\labelwidth}{#1}\n'
#              '   \\setlength{\\rightmargin}{1cm}\n'
#              '   \\setlength{\\leftmargin}{\\rightmargin}\n'
#              '   \\addtolength{\\leftmargin}{\\labelwidth}\n'
#              '   \\addtolength{\\leftmargin}{\\labelsep}\n'
#              '   \\renewcommand{\\makelabel}{\\optionlistlabel}}\n'
#              '}{\\end{list}}\n',
#              ## stylesheet is last: so it might be possible to overwrite defaults.
              self.stylesheet % (self.d_stylesheet_path),
                            ]
        if self.linking: # and maybe check for pdf
            self.pdfinfo = [ ]
            self.pdfauthor = None
            # pdftitle, pdfsubject, pdfauthor, pdfkeywords, pdfcreator, pdfproducer
        else:
            self.pdfinfo = None
        self.head = []
        self.body_prefix = ['']
#        self.body_prefix = ['\\raggedbottom\n']
        # separate title, so we can appen subtitle.
        self.title = ""
        self.body = []
        self.body_suffix = ['\n']
        self.section_level = 0
        self.context = []
        self.topic_class = ''
        # column specification for tables
        self.colspecs = []
        # verbatim: to tell encode not to encode.
        self.verbatim = 0
        # insert_newline: to tell encode to add newline.
        self.insert_newline = 0
        # mbox_newline: to tell encode to add mbox and newline.
        self.mbox_newline = 0
        # enumeration is done by list environment.
        self._enum_cnt = 0

    def language_label(self, docutil_label):
        return self.language.labels[docutil_label]

    def encode(self, text):
        """
        Encode special characters in `text` & return.
            # $ % & ~ _ ^ \ { }
        Escaping with a backslash does not help with backslashes, ~ and ^.

            < > are only available in math-mode (really ?)
            $ starts math- mode.
        AND quotes:
        
        """
        if self.verbatim:
            return text
        # first the backslash
        text = text.replace("\\", '{\\textbackslash}')
        # then dollar
        text = text.replace("$", '{\\$}')
        # then all that needs math mode
        text = text.replace("<", '{$<$}')
        text = text.replace(">", '{$>$}')
        # then
        text = text.replace("&", '{\\&}')
        text = text.replace("_", '{\\_}')
        text = text.replace("^", '{\\verb|^|}') # ugly
        text = text.replace("%", '{\\%}')
        text = text.replace("#", '{\\#}')
        text = text.replace("~", '{\\~{ }}')
        t = None
        for part in text.split('"'):
            if t == None:
                t = part
            else:
                t += self.babel.next_quote() + part
        text = t
        if self.insert_newline:
            text = text.replace("\n", '\\\\\n')
        elif self.mbox_newline:
            text = text.replace("\n", '}\\\\\n\\mbox{')
            text = text.replace(' ', '~')
        # unicode !!! 
        text = text.replace(u'\u2020', '{$\\dagger$}')
        return text

    def attval(self, text,
               whitespace=re.compile('[\n\r\t\v\f]')):
        """Cleanse, encode, and return attribute value text."""
        return self.encode(whitespace.sub(' ', text))

    def astext(self):
        if self.pdfinfo:
            if self.pdfauthor:
                self.pdfinfo.append('pdfauthor={%s}' % self.pdfauthor)
            #pdfinfo = '\\hypersetup{\n' + ',\n'.join(self.pdfinfo) + '\n}\n'
            pdfinfo = ''
        else:
            pdfinfo = ''
        title = '\\title{%s}\n' % self.title    
        return ''.join(self.head_prefix + [title] + self.head + [pdfinfo]
                       + self.body_prefix  + self.body + self.body_suffix)

    def visit_Text(self, node):
        self.body.append(self.encode(node.astext()))

    def depart_Text(self, node):
        pass

    def visit_address(self, node):
        self.visit_docinfo_item(node, 'address')

    def depart_address(self, node):
        self.depart_docinfo_item(node)

    def visit_admonition(self, node, name):
        self.body.append('\\begin{center}\n');
        # alternatives: parbox or minipage.
        # minpage has footnotes on the minipage.
        # BUG there is no border.
        self.body.append('\\parbox{\\admwidth}{\\textbf{'
                         + self.language.labels[name] + '}\n')

    def depart_admonition(self):
        self.body.append('}\n')
        self.body.append('\\end{center}\n');

    def visit_attention(self, node):
        self.visit_admonition(node, 'attention')

    def depart_attention(self, node):
        self.depart_admonition()

    def visit_author(self, node):
        self.visit_docinfo_item(node, 'author')

    def depart_author(self, node):
        self.depart_docinfo_item(node)

    def visit_authors(self, node):
        # ignore. visit_author is called for each one
        # self.visit_docinfo_item(node, 'author')
        pass

    def depart_authors(self, node):
        # self.depart_docinfo_item(node)
        pass

    def visit_block_quote(self, node):
        self.body.append( '\\begin{quote}\n')

    def depart_block_quote(self, node):
        self.body.append( '\\end{quote}\n')

    def visit_bullet_list(self, node):
        if not self.use_latex_toc and self.topic_class == 'contents':
            self.body.append( '\\begin{list}{}{}\n' )
        else:
            self.body.append( '\\begin{itemize}\n' )

    def depart_bullet_list(self, node):
        if not self.use_latex_toc and self.topic_class == 'contents':
            self.body.append( '\\end{list}\n' )
        else:
            self.body.append( '\\end{itemize}\n' )

    def visit_caption(self, node):
        self.body.append( '\\caption{\n' )
        for child in node.parent.children:
            if child.attributes.has_key('label'):
                self.body.append('\\label{%s}\n' % child.attributes['label'])

    def depart_caption(self, node):
        self.body.append('}')

    def visit_caution(self, node):
        self.visit_admonition(node, 'caution')

    def depart_caution(self, node):
        self.depart_admonition()

    def visit_citation(self, node):
        self.body.append([None, 'visit_citation'])
        #self.visit_footnote(node)

    def depart_citation(self, node):
        while self.body.pop() != [None, 'visit_citation']: pass
        #self.depart_footnote(node)

    def visit_citation_reference(self, node):
        href = ''
        if node.has_key('refid'):
            href = node['refid']
        if not href.startswith('ref-'):
            if href.find('-onpage-') > -1:
                (name, rest) = href.split('-onpage-')
                if rest.find('-') > 0:
                    cf = 'pp. %s-%s' % (rest.split('-')[0],
                                        rest.split('-')[1])
                else:
                    cf = 'p. %s' % rest

                self.body.append('\\cite[%s]{%s}' % (cf, name))
            else:
                self.body.append('\\cite{%s}' % ','.join(href.split('-andalso-')))
        else:
            self.body.append('\\ref{%s}' % href[4:])
        self.body.append(None)

        ##elif node.has_key('refname'):
        ##    href = self.document.nameids[node['refname']]
        ##self.body.append('[\\hyperlink{%s}{' % href)

    def depart_citation_reference(self, node):
        while not (self.body.pop() is None):
            pass
        ##self.body.append('}]')

    def visit_classifier(self, node):
        self.body.append( '(\\textbf{' )

    def depart_classifier(self, node):
        self.body.append( '})\n' )

    def visit_colspec(self, node):
        if self.use_longtable:
            self.colspecs.append(node)
        else:    
            self.context[-1] += 1

    def depart_colspec(self, node):
        pass

    def visit_comment(self, node,
                      sub=re.compile('\n').sub):
        """Escape end of line by a ne comment start in comment text."""
        self.body.append('%% %s \n' % sub('\n% ', node.astext()))
        raise nodes.SkipNode

    def visit_contact(self, node):
        self.visit_docinfo_item(node, 'contact')

    def depart_contact(self, node):
        self.depart_docinfo_item(node)

    def visit_copyright(self, node):
        self.visit_docinfo_item(node, 'copyright')

    def depart_copyright(self, node):
        self.depart_docinfo_item(node)

    def visit_danger(self, node):
        self.visit_admonition(node, 'danger')

    def depart_danger(self, node):
        self.depart_admonition()

    def visit_date(self, node):
        self.visit_docinfo_item(node, 'date')

    def depart_date(self, node):
        self.depart_docinfo_item(node)

    def visit_decoration(self, node):
        pass

    def depart_decoration(self, node):
        pass

    def visit_definition(self, node):
        self.body.append('%[visit_definition]\n')

    def depart_definition(self, node):
        self.body.append('\n')
        self.body.append('%[depart_definition]\n')

    def visit_definition_list(self, node):
        self.body.append( '\\begin{description}\n' )

    def depart_definition_list(self, node):
        self.body.append( '\\end{description}\n' )

    def visit_definition_list_item(self, node):
        self.body.append('%[visit_definition_list_item]\n')

    def depart_definition_list_item(self, node):
        self.body.append('%[depart_definition_list_item]\n')

    def visit_description(self, node):
        if self.use_optionlist_for_option_list:
            self.body.append( ' ' )
        else:    
            self.body.append( ' & ' )

    def depart_description(self, node):
        pass

    def visit_docinfo(self, node):
        self.docinfo = []
        self.docinfo.append('%' + '_'*75 + '\n')
        self.docinfo.append('\\begin{center}\n')
        self.docinfo.append('\\begin{tabularx}{\\admwidth}{lX}\n')

    def depart_docinfo(self, node):
        self.docinfo.append('\\end{tabularx}\n')
        self.docinfo.append('\\end{center}\n')
        self.body = self.docinfo + self.body
        # clear docinfo, so field names are no longer appended.
        self.docinfo = None
        if self.use_latex_toc:
            self.body.append('\\tableofcontents\n\n\\bigskip\n')

    def visit_docinfo_item(self, node, name):
        # should we stick to latex or docutils.
        # latex article has its own handling of date and author.
        # If we use it we get latexs language handling.
        latex_docinfo = 0
        
        if name == 'abstract':
            # NOTE tableofcontents before or after ?
            # eg after: depart_docinfo
            # NOTE this limits abstract to text.
            self.body.append('\\begin{abstract}\n')
            self.context.append('\\end{abstract}\n')
            self.context.append(self.body)
            self.context.append(len(self.body))
        else:
            self.docinfo.append('\\textbf{%s}: &\n\t' % self.language_label(name))
            if name == 'author':
                if not self.pdfinfo == None:
                    if not self.pdfauthor:
                        self.pdfauthor = self.attval(node.astext())
                    else:
                        self.pdfauthor += self.author_separator + self.attval(node.astext())
                if latex_docinfo:
                    self.head.append('\\author{%s}\n' % self.attval(node.astext()))
                    raise nodes.SkipNode
                else:
                    # avoid latexs maketitle generating one for us.
                    self.head.append('\\author{}\n')
            elif name == 'date':
                if latex_docinfo:
                    self.head.append('\\date{%s}\n' % self.attval(node.astext()))
                    raise nodes.SkipNode
                else:
                    # avoid latexs maketitle generating one for us.
                    self.head.append("\\date{}\n")
            if name == 'address':
                self.insert_newline = 1 
                self.docinfo.append('{\\raggedright\n')
                self.context.append(' } \\\\\n')
            else:    
                self.context.append(' \\\\\n')
            self.context.append(self.docinfo)
            self.context.append(len(self.body))
        # \thanks is a footnote to the title.

    def depart_docinfo_item(self, node):
        size = self.context.pop()
        dest = self.context.pop()
        tail = self.context.pop()
        tail = self.body[size:] + [tail]
        del self.body[size:]
        dest.extend(tail)
        # for address we did set insert_newline
        self.insert_newline = 0

    def visit_doctest_block(self, node):
        self.body.append( '\\begin{verbatim}' )

    def depart_doctest_block(self, node):
        self.body.append( '\\end{verbatim}\n' )

    def visit_document(self, node):
        self.body_prefix.append('\\begin{document}\n')
        self.body_prefix.append('\\maketitle\n\n')
        # alternative use titlepage environment.
        # \begin{titlepage}

    def depart_document(self, node):
        self.body_suffix.append('\\end{document}\n')

    def visit_emphasis(self, node):
        self.body.append('\\emph{')

    def depart_emphasis(self, node):
        self.body.append('}')

    def visit_entry(self, node):
        # cell separation
        column_one = 1
        if self.context[-1] > 0:
            column_one = 0
        if not column_one:
            self.body.append(' & ')

        # multi{row,column}
        if node.has_key('morerows') and node.has_key('morecols'):
            raise NotImplementedError('LaTeX can\'t handle cells that'
            'span multiple rows *and* columns, sorry.')
        atts = {}
        if node.has_key('morerows'):
            count = node['morerows'] + 1
            self.body.append('\\multirow{%d}*{' % count)
            self.context.append('}')
        elif node.has_key('morecols'):
            # the vertical bar before column is missing if it is the first column.
            # the one after always.
            if column_one:
                bar = '|'
            else:
                bar = ''
            count = node['morecols'] + 1
            self.body.append('\\multicolumn{%d}{%sl|}{' % (count, bar))
            self.context.append('}')
        else:
            self.context.append('')

        # header / not header
        if isinstance(node.parent.parent, nodes.thead):
            self.body.append('\\textbf{')
            self.context.append('}')
        else:
            self.context.append('')

    def depart_entry(self, node):
        self.body.append(self.context.pop()) # header / not header
        self.body.append(self.context.pop()) # multirow/column
        self.context[-1] += 1

    def visit_enumerated_list(self, node):
        # We create our own enumeration list environment.
        # This allows to set the style and starting value
        # and unlimited nesting.
        self._enum_cnt += 1

        enum_style = {'arabic':'arabic',
                'loweralpha':'alph',
                'upperalpha':'Alph', 
                'lowerroman':'roman',
                'upperroman':'Roman' };
        enumtype = "arabic"            
        if node.has_key('enumtype'):
            enumtype = node['enumtype']
        if enum_style.has_key(enumtype):
            enumtype = enum_style[enumtype]
        counter_name = "listcnt%d" % self._enum_cnt;
        self.body.append('\\newcounter{%s}\n' % counter_name)
        self.body.append('\\begin{list}{\\%s{%s}}\n' % (enumtype,counter_name))
        self.body.append('{\n')
        self.body.append('\\usecounter{%s}\n' % counter_name)
        # set start after usecounter, because it initializes to zero.
        if node.has_key('start'):
            self.body.append('\\addtocounter{%s}{%d}\n' \
                    % (counter_name,node['start']-1))
        ## set rightmargin equal to leftmargin
        self.body.append('\\setlength{\\rightmargin}{\\leftmargin}\n')
        self.body.append('}\n')

    def depart_enumerated_list(self, node):
        self.body.append('\\end{list}\n')

    def visit_error(self, node):
        self.visit_admonition(node, 'error')

    def depart_error(self, node):
        self.depart_admonition()

    def visit_field(self, node):
        # real output is done in siblings: _argument, _body, _name
        pass

    def depart_field(self, node):
        self.body.append('\n')
        ##self.body.append('%[depart_field]\n')

    def visit_field_argument(self, node):
        self.body.append('%[visit_field_argument]\n')

    def depart_field_argument(self, node):
        self.body.append('%[depart_field_argument]\n')

    def visit_field_body(self, node):
        # BUG by attach as text we loose references.
        if self.docinfo:
            self.docinfo.append('%s \\\\\n' % node.astext())
            raise nodes.SkipNode
        # what happens if not docinfo

    def depart_field_body(self, node):
        self.body.append( '\n' )

    def visit_field_list(self, node):
        if not self.docinfo:
            self.body.append('\\begin{quote}\n')
            self.body.append('\\begin{description}\n')

    def depart_field_list(self, node):
        if not self.docinfo:
            self.body.append('\\end{description}\n')
            self.body.append('\\end{quote}\n')

    def visit_field_name(self, node):
        # BUG this duplicates docinfo_item
        if self.docinfo:
            self.docinfo.append('\\textbf{%s}: &\n\t' % node.astext())
            raise nodes.SkipNode
        else:
            self.body.append('\\item [')

    def depart_field_name(self, node):
        if not self.docinfo:
            self.body.append(':]')

    def visit_figure(self, node):
        environment = "figure"
        for child in node.children:
            if child.attributes.has_key('environment'):
                environment = child.attributes['environment']
        self.body.append('\\begin{'+environment+'}\n')

    def depart_figure(self, node):
        environment = "figure"
        for child in node.children:
            if child.attributes.has_key('environment'):
                environment = child.attributes['environment']
        self.body.append('\n\\end{'+environment+'}\n')

    def visit_footer(self, node):
        self.context.append(len(self.body))

    def depart_footer(self, node):
        start = self.context.pop()
        footer = (['\n\\begin{center}\small\n']
                  + self.body[start:] + ['\n\\end{center}\n'])
        self.body_suffix[:0] = footer
        del self.body[start:]

    def visit_footnote(self, node):
        notename = node['id']
        self.body.append(None)

    def depart_footnote(self, node):
        list = []
        while 1:
            el = self.body.pop()
            if el is None: break
            list.insert(0, el)

        i = self.body.index('!footnote:%s!' % node['id'])
        self.body[i:i+1] = ['\\footnote{'] + list[3:] + ['}']

        if i>0 and self.body[i-1][-1] == ' ':
            self.body[i-1] = self.body[i-1][:-1]

    def visit_footnote_reference(self, node):
        href = ''
        if node.has_key('refid'):
            href = node['refid']

        self.body.append('!footnote:%s!' % href)
            
        #elif node.has_key('refname'):
        #    href = self.document.nameids[node['refname']]
        #format = self.settings.footnote_references
        #if format == 'brackets':
        #    suffix = '['
        #    self.context.append(']')
        #elif format == 'superscript':
        #    suffix = '\\raisebox{.5em}[0em]{\\scriptsize'
        #    self.context.append('}')
        #else:                           # shouldn't happen
        #    raise AssertionError('Illegal footnote reference format.')
        #self.body.append('%s\\hyperlink{%s}{' % (suffix,href))

    def depart_footnote_reference(self, node):
        self.body.pop() # remove footnote number, inserted by TeX
        #self.body.append('}%s' % self.context.pop())

    def visit_generated(self, node):
        pass

    def depart_generated(self, node):
        pass

    def visit_header(self, node):
        self.context.append(len(self.body))

    def depart_header(self, node):
        start = self.context.pop()
        self.body_prefix.append('\n\\verb|begin_header|\n')
        self.body_prefix.extend(self.body[start:])
        self.body_prefix.append('\n\\verb|end_header|\n')
        del self.body[start:]

    def visit_hint(self, node):
        self.visit_admonition(node, 'hint')

    def depart_hint(self, node):
        self.depart_admonition()

    def visit_image(self, node):
        atts = node.attributes.copy()
        if not atts.has_key('environment') or \
               (atts.has_key('environment') and \
                not atts['uri'] == '__extended__'):
            href = atts['uri']
            self.body.append('\\centering\n')
            self.body.append('\\includegraphics')
            if atts.has_key('width'): self.body.append('[width=%s]' % atts['width'])
            else: self.body.append('[width=\\columnwidth]')
            self.body.append('{%s}\n' % href)
        ##self.body.append('\\end{center}\n')

    def depart_image(self, node):
        pass

    def visit_important(self, node):
        self.visit_admonition(node, 'important')

    def depart_important(self, node):
        self.depart_admonition()

    def visit_interpreted(self, node):
        # @@@ Incomplete, pending a proper implementation on the
        # Parser/Reader end.
        # For now, pass through as LaTeX.
        self.body.append(node.astext())
        raise nodes.SkipNode

    def depart_interpreted(self, node):
        pass

    def visit_label(self, node):
        # footnote/citation label
        self.body.append('[')

    def depart_label(self, node):
        self.body.append(']')

    def visit_legend(self, node):
        self.body.append('{\\small ')

    def depart_legend(self, node):
        self.body.append('}')

    def visit_line_block(self, node):
        """line-block: 
        * whitespace (including linebreaks) is significant 
        * inline markup is supported. 
        * serif typeface"""
        self.mbox_newline = 1
        self.body.append('\\begin{flushleft}\n\\mbox{')

    def depart_line_block(self, node):
        self.body.append('}\n\\end{flushleft}\n')
        self.mbox_newline = 0

    def visit_list_item(self, node):
        self.body.append('\\item ')

    def depart_list_item(self, node):
        self.body.append('\n')

    def visit_literal(self, node):
        self.body.append('\\texttt{')

    def depart_literal(self, node):
        self.body.append('}')

    def visit_literal_block(self, node):
        self.use_verbatim_for_literal = 1
        if (self.use_verbatim_for_literal):
            self.verbatim = 1
            self.body.append('\\begin{quote}\n')
            self.body.append('\\begin{verbatim}\n')
        else:
            self.body.append('{\\obeylines\\obeyspaces\\ttfamily\n')

    def depart_literal_block(self, node):
        if self.use_verbatim_for_literal:
            self.body.append('\n\\end{verbatim}\n')
            self.body.append('\\end{quote}\n')
            self.verbatim = 0
        else:
            self.body.append('}\n')

    def visit_meta(self, node):
        self.body.append('[visit_meta]\n')
        # BUG maybe set keywords for pdf
        ##self.head.append(self.starttag(node, 'meta', **node.attributes))

    def depart_meta(self, node):
        self.body.append('[depart_meta]\n')

    def visit_note(self, node):
        self.visit_admonition(node, 'note')

    def depart_note(self, node):
        self.depart_admonition()

    def visit_option(self, node):
        if self.context[-1]:
            # this is not the first option
            self.body.append(', ')

    def depart_option(self, node):
        # flag tha the first option is done.
        self.context[-1] += 1

    def visit_option_argument(self, node):
        """The delimiter betweeen an option and its argument."""
        self.body.append(node.get('delimiter', ' '))

    def depart_option_argument(self, node):
        pass

    def visit_option_group(self, node):
        if self.use_optionlist_for_option_list:
            self.body.append('\\item [')
        else:
            atts = {}
            if len(node.astext()) > 14:
                self.body.append('\\multicolumn{2}{l}{')
                self.context.append('} \\\\\n  ')
            else:
                self.context.append('')
            self.body.append('\\texttt{')
        # flag for first option    
        self.context.append(0)

    def depart_option_group(self, node):
        self.context.pop() # the flag
        if self.use_optionlist_for_option_list:
            self.body.append('] ')
        else:
            self.body.append('}')
            self.body.append(self.context.pop())

    def visit_option_list(self, node):
        self.body.append('% [option list]\n')
        if self.use_optionlist_for_option_list:
            self.body.append('\\begin{optionlist}{3cm}\n')
        else:
            self.body.append('\\begin{center}\n')
            # BUG: use admwidth or make it relative to textwidth ?
            self.body.append('\\begin{tabularx}{.9\\linewidth}{lX}\n')

    def depart_option_list(self, node):
        if self.use_optionlist_for_option_list:
            self.body.append('\\end{optionlist}\n')
        else:
            self.body.append('\\end{tabularx}\n')
            self.body.append('\\end{center}\n')

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        if not self.use_optionlist_for_option_list:
            self.body.append('\\\\\n')

    def visit_option_string(self, node):
        ##self.body.append(self.starttag(node, 'span', '', CLASS='option'))
        pass

    def depart_option_string(self, node):
        ##self.body.append('</span>')
        pass

    def visit_organization(self, node):
        self.visit_docinfo_item(node, 'organization')

    def depart_organization(self, node):
        self.depart_docinfo_item(node)

    def visit_paragraph(self, node):
        if not self.topic_class == 'contents':
            self.body.append('\n')

    def depart_paragraph(self, node):
        if self.topic_class == 'contents':
            self.body.append('\n')
        else:
            self.body.append('\n')

    def visit_problematic(self, node):
        self.body.append('{\\color{red}\\bfseries{}')

    def depart_problematic(self, node):
        self.body.append('}')

    def visit_raw(self, node):
        if node.has_key('format') and node['format'].lower() == 'latex':
            self.body.append(node.astext())
        raise nodes.SkipNode

    def visit_reference(self, node):
        # for pdflatex hyperrefs might be supported
        if node.has_key('refuri'):
            href = node['refuri']
        elif node.has_key('refid'):
            href = '#' + node['refid']
        elif node.has_key('refname'):
            href = '#' + self.document.nameids[node['refname']]
        ##self.body.append('[visit_reference]')
        self.body.append('\\href{%s}{' % href)

    def depart_reference(self, node):
        self.body.append('}')
        ##self.body.append('[depart_reference]')

    def visit_revision(self, node):
        self.visit_docinfo_item(node, 'revision')

    def depart_revision(self, node):
        self.depart_docinfo_item(node)

    def visit_row(self, node):
        self.context.append(0)

    def depart_row(self, node):
        self.context.pop()  # remove cell counter
        self.body.append(' \\\\ \\hline\n')

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_status(self, node):
        self.visit_docinfo_item(node, 'status')

    def depart_status(self, node):
        self.depart_docinfo_item(node)

    def visit_strong(self, node):
        self.body.append('\\textbf{')

    def depart_strong(self, node):
        self.body.append('}')

    def visit_substitution_definition(self, node):
        raise nodes.SkipNode

    def visit_substitution_reference(self, node):
        self.unimplemented_visit(node)

    def visit_subtitle(self, node):
        self.title = self.title + \
                '\\\\\n\\large{%s}\n' % self.encode(node.astext()) 
        raise nodes.SkipNode

    def depart_subtitle(self, node):
        pass

    def visit_system_message(self, node):
        if node['level'] < self.document.reporter['writer'].report_level:
            raise nodes.SkipNode


    def depart_system_message(self, node):
        self.body.append('\n')

    def visit_title_reference(self, node):
        return self.visit_interpreted(node)

    def depart_title_reference(self, node):
        return self.depart_interpreted(node)

    def get_colspecs(self):
        """
        Return column specification for longtable.

        The width is scaled down by 93%. We do it here
        because the we can use linewidth which should be the local
        width.
        """
        width = 0
        for node in self.colspecs:
            width += node['colwidth']
        s = ""
        for node in self.colspecs:
            colwidth = 0.93 * float(node['colwidth']) / width 
            s += "|p{%.2f\\linewidth}" % colwidth
        self.colspecs = []
        return s+"|"

    def visit_table(self, node):
        if self.use_longtable:
            self.body.append('\n\\begin{longtable}[c]')
        else:
            self.body.append('\n\\begin{tabularx}{\\linewidth}')
            self.context.append('table_sentinel') # sentinel
            self.context.append(0) # column counter

    def depart_table(self, node):
        if self.use_longtable:
            self.body.append('\\end{longtable}\n')
        else:    
            self.body.append('\\end{tabularx}\n')
            sentinel = self.context.pop()
            if sentinel != 'table_sentinel':
                print 'context:', self.context + [sentinel]
                raise AssertionError

    def table_preamble(self):
        if self.use_longtable:
            self.body.append('{%s}\n' % self.get_colspecs())
        else:
            if self.context[-1] != 'table_sentinel':
                self.body.append('{%s}' % ('|X' * self.context.pop() + '|'))
                self.body.append('\n\\hline')

    def visit_target(self, node):
        if not (node.has_key('refuri') or node.has_key('refid')
                or node.has_key('refname')):
            #self.body.append('\\hypertarget{%s}{' % node['name'])
            self.context.append('}')
        else:
            self.context.append('')

    def depart_target(self, node):
        self.body.append(self.context.pop())

    def visit_tbody(self, node):
        # BUG write preamble if not yet done (colspecs not [])
        # for tables without heads.
        if len(self.colspecs) > 0:
            self.visit_thead(None)
            self.depart_thead(None)
        self.body.append('%[visit_tbody]\n')

    def depart_tbody(self, node):
        self.body.append('%[depart_tbody]\n')

    def visit_term(self, node):
        self.body.append('\\item[')

    def depart_term(self, node):
        # definition list term.
        self.body.append(':]\n')

    def visit_tgroup(self, node):
        #self.body.append(self.starttag(node, 'colgroup'))
        #self.context.append('</colgroup>\n')
        pass

    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        # number_of_columns will be zero after get_colspecs.
        # BUG ! push onto context for depart to pop it.
        number_of_columns = len(self.colspecs)
        self.table_preamble()
        #BUG longtable needs firstpage and lastfooter too.
        self.body.append('\\hline\n')

    def depart_thead(self, node):
        if self.use_longtable:
            # the table header written should be on every page
            # => \endhead
            self.body.append('\\endhead\n')
            # and the firsthead => \endfirsthead
            # BUG i want a "continued from previous page" on every not
            # firsthead, but then we need the header twice.
            #
            # there is a \endfoot and \endlastfoot too.
            # but we need the number of columns to 
            # self.body.append('\\multicolumn{%d}{c}{"..."}\n' % number_of_columns)
            # self.body.append('\\hline\n\\endfoot\n')
            # self.body.append('\\hline\n')
            # self.body.append('\\endlastfoot\n')
            

    def visit_tip(self, node):
        self.visit_admonition(node, 'tip')

    def depart_tip(self, node):
        self.depart_admonition()

    def visit_title(self, node):
        """Only 3 section levels are supported by LaTeX article (AFAIR)."""
        if node.astext().lower().strip() == 'abstract':
            self.body.append('\\abstract')
            raise nodes.SkipNode
        
        if isinstance(node.parent, nodes.topic):
            # section titles before the table of contents.
            if node.parent.hasattr('id'):
                pass
                #self.body.append('\\hypertarget{%s}{}' % node.parent['id'])
            self.body.append('\\begin{center}\n')
            self.context.append('\\end{center}\n')
            ## should this be section subsection or 
            self.body.append('\\subsection*{')
            self.context.append('}\n')
        elif self.section_level == 0:
            # document title
            self.title = self.encode(node.astext())
            if not self.pdfinfo == None:
                self.pdfinfo.append( 'pdftitle={%s}' % self.encode(node.astext()) )
            raise nodes.SkipNode
        else:
            self.body.append('\n\n')
            self.body.append('%' + '_' * 75)
            self.body.append('\n\n')
            if node.parent.hasattr('id'):
                pass
                #self.body.append('\\hypertarget{%s}{}\n' % node.parent['id'])
            # section_level 0 is title and handled above.    
            # BUG: latex has no deeper sections (actually paragrah is no section either).
#            if self.use_latex_toc:
            section_star = ""
#            else:
#                 section_star = "*"
            secl = self.section_level
            if self.settings.documentclass in ['book', 'report']: secl = secl-1

            if secl == 0:
                self.body.append('\\chapter%s{' % (section_star))
            elif (secl<=3):  # 1,2,3
                self.body.append('\\%ssection%s{' % ('sub'*(secl-1),section_star))
            elif (secl==4):      
                #self.body.append('\\paragraph*{')
                self.body.append('\\subsubsection%s{' % (section_star))
            else:
                #self.body.append('\\subparagraph*{')
                self.body.append('\\subsubsection%s{' % (section_star))
            # BUG: self.body.append( '\\label{%s}\n' % name)
            self.context.append('}\n')

    def depart_title(self, node):
        self.body.append(self.context.pop())
        if isinstance(node.parent, nodes.topic):
            self.body.append(self.context.pop())
        # BUG level depends on style.
        if node.parent.hasattr('id') and not self.use_latex_toc:
            # pdflatex allows level 0 to 3
            # ToC would be the only on level 0 so i choose to decrement the rest.
            # "Table of contents" bookmark to see the ToC. To avoid this
            # we set all zeroes to one.
            l = self.section_level
            if l>0:
                l = l-1
            self.body.append('\\pdfbookmark[%d]{%s}{%s}\n' % \
                (l,node.astext(),node.parent['id']))

    def visit_topic(self, node):
        self.topic_class = node.get('class')
        if self.use_latex_toc:
            self.topic_class = ''
            raise nodes.SkipNode

    def depart_topic(self, node):
        self.topic_class = ''
        self.body.append('\n')

    def visit_transition(self, node):
        self.body.append('\n\n')
        self.body.append('%' + '_' * 75)
        self.body.append('\n\\hspace*{\\fill}\\hrulefill\\hspace*{\\fill}')
        self.body.append('\n\n')

    def depart_transition(self, node):
        #self.body.append('[depart_transition]')
        pass

    def visit_version(self, node):
        self.visit_docinfo_item(node, 'version')

    def depart_version(self, node):
        self.depart_docinfo_item(node)

    def visit_warning(self, node):
        self.visit_admonition(node, 'warning')

    def depart_warning(self, node):
        self.depart_admonition()

    def unimplemented_visit(self, node):
        raise NotImplementedError('visiting unimplemented node type: %s'
                                  % node.__class__.__name__)

#    def unknown_visit(self, node):
#    def default_visit(self, node):
    
# vim: set ts=4 et ai :
