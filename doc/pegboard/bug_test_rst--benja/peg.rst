=============================================================
``bug_test_rst--benja``: Marking failing tests to use ReST
=============================================================

:Author:   	Benja Fallenstein
:Last-Modified: $Date: 2003/04/25 08:23:05 $
:Revision: 	$Revision: 1.2 $
:Status:   	Accepted


Tuomas' "`Handling Bugs`_" PEG specifies that an RFC 2822-like
syntax should be used to mark failing PEGs. However,

- RFC 2822 headers are supposed to be at the beginning of
  something; putting them at the end of something
  (as "Handling Bugs" does) isn't really well-specified
  and needs our own parser.
- These headers aren't meant to be used in docstrings.

Therefore, I propose to use reStructuredText_ field lists
instead. They're designed to be very much like RFC 2822 headers,
but can appear anywhere in a reST fragment-- and reStructuredText 
was designed for use in Python docstrings.

.. _Handling Bugs: ../bug_test--tjl/peg.gen.html
.. _reStructuredText: http://docutils.sourceforge.net/rst.html

\- Benja
