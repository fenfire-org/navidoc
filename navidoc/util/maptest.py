# 
# Copyright (c) 2003, Tuomas J. Lukka
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
# 

# Generic tests for maps that keep at least 5 keys.


def setUp_maptest(map):
    global theMap
    theMap = map

def test_maptest_ops():
    v = [i for i in range(0,10)]

    theMap.put("A", v[0])
    assert theMap.get("A") == v[0]
    assert theMap.get("B") == None
    assert theMap.get(None) == None
    assert theMap.containsKey("A")
    assert not theMap.containsKey("B")
    assert not theMap.isEmpty()
    assert theMap.remove("A") == v[0]
    assert theMap.get("A") == None
    assert theMap.isEmpty()

