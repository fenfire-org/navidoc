#
# Copyright (c) 2002, Benja Fallenstein and Tuomas J. Lukka
# 
# This file is part of Fenfire.
# 
# Fenfire is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# Fenfire is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General
# Public License along with Fenfire; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
# 
#

"""
Test.py -- load *.test files and execute tests in them.

The directory containing .test files to be run is passed as a parameter.
(Can also be more than one.)

Here, I liked the trivial test suites in lava/ far too much to let them go
(the nice thing was that you could just make a plain text file and
start writing tests into it). So, here's a tool that looks for *.test
files in the test/ subtree and turns them into unittest classes.
Let's try to incrementally make it as comfortable as possible.

One thing I'd really like would be *.spec files that are Ly files which
can be tangled into unittests...
"""
import sys
#sys.path.insert(0, ".")
import os.path, imp
import getopt
import fnmatch
import re
import traceback

def test(module):
    tests = [test for test in dir(module) if test.startswith('test')]
    exceptions = []

    for test in tests:
        fn = getattr(module, test)
	rawname = '%s.%s' % (module.__name__, test)

        if not fn.__doc__:
            name = rawname
        else:
            lines = fn.__doc__.split('\n')
            if lines[0] == '':
                name = '%s.%s (%s)' % (module.__name__, test,
                                       lines[1].strip())
            else:
                name = '%s.%s (%s)' % (module.__name__, test,
                                       lines[0].strip())
        
        print name + "... ",

        try:
            if hasattr(module, 'setUp'): module.setUp()
            fn()
            if hasattr(module, 'tearDown'): module.tearDown()
        except:
            print "failed."
            exceptions.append([name, {
                'exception': sys.exc_info(),
                'test': test,
                'testname': name,
            }])
        else:
            print "ok."

    return exceptions

def load(file):
    name = os.path.splitext(file)[0]

    while name.startswith('.') or name.startswith('/'):
        name = name[1:]
    
    name = '.'.join(name.split('/'))
    name = '.'.join(name.split('\\'))

    module = imp.new_module(name)
    execfile(file, module.__dict__)
    return module

    

def tests(files):
    """
    Return a list of all *.test files in a given directory and its
    subdirectories.
    """

    def addTests(list, dirname, names):
	if dirname[0] in [',', '{']: return
	if len(dirname) > 2 and dirname[2] in [',', '{']: return
        names = [n for n in names if fnmatch.fnmatch(n, '*.test')]
        names = [os.path.join(dirname, name) for name in names]
        list.extend(names)

    tests = []
    for f in files:
        if os.path.isdir(f):
            os.path.walk(f, addTests, tests)
        else:
            tests.append(f)
    return tests


if __name__ == '__main__':
    dirs = sys.argv[1:]

    exceptions = []

    for file in tests(dirs):
        loaded = load(file)
        exceptions.extend(test(loaded))

    if exceptions:
        print "Python stack traces:"
        for name, exc in exceptions:
            print 75 * '-'
            print name
            traceback.print_exception(*exc['exception'])
            
            print 75 * '-'
            print

    print "%s test failures." % len(exceptions)
