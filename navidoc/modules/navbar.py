#
# Copyright (c) 2003 by Benja Fallenstein
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

#$Id: navbar.py,v 1.13 2003/05/22 10:52:21 humppake Exp $

#
# Written by Benja Fallenstein
#

__docformat__ = 'reStructuredText'

import config

import re, os

from navidoc.util.path import *

dbg = config.dbg.shorthand('navbar')

class Tree:
    re_title = re.compile("<title>(.*)</title>")

    def __init__(self, dir):
        self.root = dir
        self.files = []
        self.name = None

        dirlist = os.listdir(self.root);
        dirlist.sort()

        for el in dirlist:
            el = os.path.join(self.root, el)
            if os.path.isdir(el):
                if os.path.exists(os.path.join(el, 'index.rst')):
                    self.addDir(el)
            elif os.path.splitext(el)[1] == '.html':
                self.addFile(el)
    
    def addFile(self, filename, contents=None):
        if contents is None:
            file = open(filename)
            contents = file.read()
            file.close()
        
        match = self.re_title.search(contents)
        if not match:
            dbg(("File %s skipped: It does not contain "
                   "a <title>.") % filename)
            return

        name = match.group(1)
        
        if os.path.basename(filename) in ('index'+config.midfix+'.html',
                                          'peg'+config.midfix+'.html'):
            self.name = name

        self.files.append([filename, name])

    def addDir(self, dir):
        t = Tree(dir)
        if len(t.files) > 0 or t.name != None:
            self.files.append([dir, t.name, t])

    def prettyprint(self, indent=""):
        for el in self.files:
            dbg("%s%s [%s]" % (indent, el[1],
                               os.path.basename(el[0])))
            if len(el) > 2:
                el[2].prettyprint(indent+"  ")

    def getFiles(self):
        list = []
        for el in self.files:
            if len(el) == 2: list.append(el[0])
            else: list.extend(el[3].getFiles())

def simpleNavbar(tree, filepath, indent=""):
    s = ""
    for el in tree.files:
        if el[0].endswith('index.html'): continue
        s += '<li class="boxitem"><a href="%s">%s</a></li>\n' % \
             (relative_path(filepath, el[0]), el[1])
        if len(el) > 2:
            s += "<ul>\n"
            s += simpleNavbar(el[2], filepath, indent+"&nbsp;&nbsp;")
            s += "</ul>\n"
    return s

def getBar(tree, filepath):
    bar = '<!-- NavBar begin -->\n<hr class="footer"/>\n'
    bar += '<center class="navigation-title">Navigation</center>\n'
    bar += '<div class="left">\n'
    bar += '<div class="left-bar">\n'
    bar += ('<p class="boxhead"><a href="%s">%s'
            '</a></p>\n') \
            % (relative_path(filepath, slashify(tree.root)),
               tree.name)
    bar += '<p class="boxcontent"><ul>\n'
    bar += simpleNavbar(tree, filepath=filepath)
    bar += '</ul></p></div>\n'
    bar += '<div class="logo-bar" style="text-align: center">\n'
    bar += ('<a href="%s"><img src="%s" alt="The Fenfire logo '
            '(a purple flame)"/></a></div>\n') \
            % (relative_path(filepath, slashify(tree.root)),
               relative_path(filepath, slashify(tree.root)+'logo.png'))
    bar += '</div>\n<!-- NavBar end -->\n'
    return bar

def insertNavbars(tree, navbarTree=None, singleFile=None):
    if navbarTree == None: navbarTree = tree
    if singleFile:
        file = open(el[0]); s = file.read(); file.close()

        # Trys to find possible existing navbar first and replace that
        i = s.find('<!-- NavBar begin -->'+"\n")
        e = s.find('<!-- NavBar end -->'+"\n") + len('<!-- NavBar end -->'+"\n")
        if (i == -1): i = s.find('<hr class="footer"/>'); e = i

        s = s[:i] + getBar(navbarTree, el[0]) + s[e:]
        file = open(el[0], 'w')
        file.write(s)
        file.close()
        dbg("Inserted navbar into %s" % filename)

    else:
        for el in tree.files:
            if len(el) == 2:
                file = open(el[0]); s = file.read(); file.close()

                # Tries to find possible existing navbar first and replace that
                i = s.find('<!-- NavBar begin -->'+"\n")
                e = s.find('<!-- NavBar end -->'+"\n") + len('<!-- NavBar end -->'+"\n")
                if (i == -1): i = s.find('<hr class="footer"/>'); e = i

                s = s[:i] + getBar(navbarTree, el[0]) + s[e:]
                file = open(el[0], 'w')
                file.write(s)
                file.close()
                dbg( "Inserted navbar into %s" % el[0])
            else:
                insertNavbars(el[2], navbarTree)

if __name__ == '__main__':
    import sys
    t = Tree(sys.argv[1])
    insertNavbars(t)

def postprocess(path):
    t = Tree(path)
    insertNavbars(t)
