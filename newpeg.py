#!/usr/bin/env python

# 
# Copyright (c) 2002, 2003 by Asko Soukka
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

#$Id: newpeg.py,v 1.4 2003/07/28 13:53:51 tjl Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
A simple script for creating a new PEG.
"""

import config
config.read_config(config, 'navidoc.conf')

from navidoc.util.path import *

import sys, re, os, os.path, time

def parse_peg_name(peg_name):
    peg_namefilter = re.compile('[a-zедц_1-90]*')
    peg_nameparts = peg_namefilter.findall(peg_name)
    while peg_nameparts.count(''): peg_nameparts.remove('')
    return peg_nameparts

peg_path = ''
peg_author_nick = ''
peg_author = ''

if len(sys.argv) > 1:
    if os.path.isdir(sys.argv[1]):
        peg_path = sys.argv[1]

print """
****************************************
Give a descriptive id for the new PEG.
Please,use format "peg_name--author".
****************************************
"""

peg_name = parse_peg_name(raw_input().lower())

if len(peg_name) > 1:
    peg_author_nick = peg_name.pop(-1)
    
assert peg_author_nick != '', """
PEG must have an author.
In a PEG name, the author is separated with "--".
"""     

for name, nick in config.pegboard_authors.items():
    if nick == peg_author_nick:
        peg_author = name

peg_dir = '_'.join([part for part in peg_name])

assert not os.path.isdir(slashify(peg_path)+peg_dir+'--'+peg_author_nick), """
The proposed PEG directory %s already exists!
""" % (slashify(peg_path)+peg_dir+'--'+peg_author_nick)

print """
***************************************
Press Enter to create the following PEG
or enter any other key to cancel.

Peg name: %s
Peg directory: %s%s
Author: %s (%s)
****************************************
""" % (peg_dir,
       slashify(peg_path),
       peg_dir+'--'+peg_author_nick,
       peg_author_nick,
       peg_author)

assert raw_input().lower() == '', """ 
Interrupted by user.
"""

print 'Creating a new directory %s.' % \
      (slashify(peg_path)+peg_dir+'--'+peg_author_nick)
os.mkdir(slashify(peg_path)+peg_dir+'--'+peg_author_nick)

print 'Creating peg.rst template.'
out = open(slashify(slashify(peg_path)+peg_dir+'--'+peg_author_nick) \
           +'peg.rst', 'w')
localtime = time.localtime()
date = '%s-%02d-%02d' % (localtime[0], localtime[1], localtime[2])
out.write("""
==========================================================================
PEG %s--%s:
==========================================================================

:Authors:  %s
:Date-Created: %s
:Last-Modified: $Date: 2003/07/28 13:53:51 $
:Revision: $Revision: 1.4 $
:Status:   Incomplete

.. :Stakeholders:
.. :Scope:    Major|Minor|Trivial|Cosmetic
.. :Type:     META|Policy|Architecture|Interface|Implementation

.. Affect-PEGs:


The PEG should begin with the header and after that, a short
introduction which should briefly answer the questions what and why
(and, if not obvious, how).

Issues
======

There should be an Issues section (following the example of OpenGL
extension specs), which should contain the open questions related to
this PEG. Once an issue is resolved, it is often good to leave the
resolution and the rationale behind the resolution into the Issues
section

Changes
=======

Then, there can be free-form sections in which the changes proposed
are detailed.

""" % (peg_dir,
       peg_author_nick,
       peg_author,
       date))
out.close()

print 'Creating .cvsignore.'
out = open(slashify(slashify(peg_path)+peg_dir+'--'+peg_author_nick) \
           +'.cvsignore', 'w')
out.write('*.gen.*'+"\n")
out.close()

print """
Creation of PEG template completed.
%s
""" % (slashify(peg_path)+peg_dir+'--'+peg_author_nick)
