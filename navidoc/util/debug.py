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

#$Id: debug.py,v 1.3 2003/06/30 13:56:10 humppake Exp $

#
# Written by Asko Soukka
#

__docformat__ = 'reStructuredText'

"""
Navidoc debug.
"""

class DebugFilter:
    """
    Navidoc debug stream handler class.
    """

    short = "d:D:"
    long = ["--dbg="]
    all = ["-d", "-D"] + long

    output_enabled = {}
    buffer = {}

    def __init__(self):
        pass

    def enable(self, dbg_name):
        """
        enable(self, dbg_name)
        
        Enable output of a named debug stream.
        """
        self.output_enabled[dbg_name] = 1

    def mute(self, dbg_name):
        """
        mute(self, dbg_name)
        
        Mute output of a named debug stream.
        """
        self.output_enabled[dbg_name] = 0

    def out(self, dbg_name, dbg_str):
        """
        out(self, dbg_name, dbg_str)

        Print string to a named debug stream.
        If the debug stream is muted, add string into
        its buffer.
        """
        if self.output_enabled.has_key(dbg_name) \
               and self.output_enabled[dbg_name]:
            print "[", dbg_name, "]", dbg_str
        else:
            if not self.buffer.has_key(dbg_name):
                self.buffer['dbg_name'] = []
            self.buffer['dbg_name'].append(dbg_str)

    def shorthand(self, dbg_name):
        """
        shorthand(self, dbg_name)

        Return shorthand for use of a named debug stream.
        """
        return lambda dbg_string, self=self, dbg_name=dbg_name: \
                                        self.out(dbg_name, dbg_string)

    def flush(self, dbg_name):
        """
        flush(self, dbg_name)

        Flush the buffer of a named debug stream.
        """
        if self.buffer.has_key(dbg_name):
            for line in self.buffer['dbg_name']:
                print "[", dbg_name, "]", line
            self.buffer['dbg_name'] = []
