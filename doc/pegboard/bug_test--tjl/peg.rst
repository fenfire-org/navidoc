=============================================================
PEG bug_test--tjl: Handling bugs
=============================================================

:Author:   Tuomas Lukka
:Last-Modified: $Date: 2003/03/31 09:32:00 $
:Revision: $Revision: 1.1 $
:Status:   Implemented

Making failing tests for bugs is not currently handled very
well. This PEG proposes a relatively simple way to handle it.

Issues
======

    * Should we use the test name or the docstring for tagging?

        RESOLVED: Docstring. This gives us easier extensibility
	and avoids the "breaking of test after it passes" 
	problem this PEG is meant to prevent.

    * What conventions should there be for encoding the failing of tests?
	
	RESOLVED: A bit like rfc822. Extensibility.

    * Should we be able to tag separately tests failing in AWT,
      tests failing in GL and both?

	RESOLVED: Yes. It's very good to be able to say in the
	test that "this works in GL, but doesn't in AWT" so that
	the normal testrunner *will* run the test for GL.

Bug tests
=========

Starting from the following:

    1) Unit tests are important for seeing if things still work
       correctly, after a given change. Therefore, it must be clear
       whether things went in the expected way or not.

    2) We want to be able to make failing tests for bugs before fixing
       them

    3) Making failing tests in separate files or so is impractical
       and can lead to mistakes when moving tests (e.g. the framework).

The proposal is that we encode whether a given test is failing into
the test docstring.

For example, ::

    def testFoo(): # run test always
	"""Test that foo does X correctly.
	"""
	pass

    def testBar(): # this test is known to fail on AWT.
	"""Test that bar does Y in the right way, 
	if gloob is bree.

	fail: AWT
	"""

	pass

Currently, the alternatives for the "fail" line are ::

    fail: AWT
    fail: GL
    fail: *


Then, the Makefile targets should be adjusted as follows::

    make test		# Run all tests that should succeed on AWT
    make test-gl	# Run all tests that should succeed on GL

    make testbugs	# Run all tests that should fail on AWT
    make testbugs-gl	# Run all tests that should fail on GL

