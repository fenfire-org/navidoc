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

#$Id: path.py,v 1.4 2003/06/30 13:56:10 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

import os.path

def listdir(path, extensions, dirs=0):
    """
    listdir(path, extensions, dirs=0)

    Quite specialized listdir, which return all directories and files
    with specific extensions under given path. Nonrecursive.

    Skipping files starting with '.' or including some of 'CVS', '#', '~'.
    """
    files = [f for f in os.listdir(path) if not f.startswith('.')
             and not f == 'CVS' and '#' not in f and '~' not in f]

    if extensions:
        files = [f for f in files if extensions.count(f.split('.')[-1]) > 0 \
                 or os.path.isdir(slashify(path)+f)]
    if not dirs:
        files = [f for f in files if os.path.isfile(slashify(path)+f)]
    return files

def slashify(path):
    """
    slashify(path)

    End path with a trailing slash, if still necessary.
    """
    if len(path) > 0:
        return (path+'/').replace('//','/')
    return path

def relative_path(source, target):
    """
    relative_path(source, target)

    Return a relative filepath from the source filepath to the target
    filepath.
    """
    import config
    dbg = config.dbg.shorthand('path')

    if source == None or len(source) == 0: return target

    source = os.path.normpath(os.path.abspath(source))
    target = os.path.normpath(os.path.abspath(target))

    if os.path.isdir(source): source = slashify(source)
    if os.path.isdir(target): target = slashify(target)

    dbg('Source: %s, Target: %s' % (source, target)) 

    depth = source.count('/')
    source_parts = source.split('/')
    target_parts = target.split('/')

    parts = len(source_parts) < len(target_parts) \
            and len(source_parts) or len(target_parts)

    for i in range(parts):
        if source_parts[i] != target_parts[i]:
            parts = i
            break

    relative = ''.join(['../' for i in range(depth-parts)]) \
               +''.join([target_parts[i+parts]+'/' \
                         for i in range(len(target_parts)-parts)])

    path = relative[0:len(relative)-1]

    if path=='' and os.path.isdir(target): path = './'
    elif path == '': path = os.path.basename(target)

    dbg('Relative path: '+path)
    return (path)
