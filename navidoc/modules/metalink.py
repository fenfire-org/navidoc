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

#$Id: metalink.py,v 1.5 2003/06/17 12:04:04 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

import os.path

from navidoc.util.path import *

def postprocess(path):
    """
    HTML postprocessing function to add <link> tags into
    target filename.
    """

    dirlist = listdir(path, "html", dirs=1)
    dirlist.sort()
    location = 0

    for entry in dirlist:        
        if os.path.isdir(slashify(path)+entry) \
               and not os.path.islink(slashify(path)+entry):
            postprocess(slashify(path)+entry)

        if os.path.isfile(slashify(path)+entry):
            html_file = open(slashify(path)+entry)
            html = html_file.read()
            html_file.close()

            insert = html.lower().find("</head>")
            out = open(slashify(path)+entry, "w")
            out.write(html[0:insert])

            #out.write('<meta name="robots" content="noarchive, noindex, nofollow" />'+"\n")
            #out.write('<link rel="top" href="'+top+'" />'+"\n")
            #out.write('<link rel="copyright" href="'+copyright+'" />'+"\n")

            if len(path.split('/')) > 1:
                out.write('<link rel="up" href="../" />'+"\n")
            out.write('<link rel="index" href="./" />'+"\n")
            if location > 0:
                out.write('<link rel="first" href="'+dirlist[0]+'" />'+"\n")
            if location > 0:
                out.write('<link rel="prev" href="'+dirlist[location-1]+'" />'+"\n")
            if location < len(dirlist)-1:
                out.write('<link rel="next" href="'+dirlist[location+1]+'" />'+"\n")
            if location < len(dirlist)-1:
                out.write('<link rel="last" href="'+dirlist[len(dirlist)-1]+'" />'+"\n")

            out.write(html[insert:len(html)])
            out.close()
        location+=1
