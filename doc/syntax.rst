==========
UML syntax
==========

Defining UML diagram begins like any directive definition in reStructuredText::

   .. UML:: foobar

After the definition follows an indented content. The content should
contain definition part and usually also layout part.

Definition
==========

There are several possibilities for definition of UML elements. The
first variant is the most clearest, but the others allow explict
definition of variables for elements. After the first definition the
element is referred using its name, after the later definitions the
element is referred using its variable.

.. UML:: syntax-defining-1

   class foo

Syntax::

   class foo

.. UML:: syntax-defining-2

   foo = class foo123

Syntax::

   foo = class foo123

.. UML:: syntax-defining-3

   class (foo) foo123

Syntax::

   class (foo) foo123

Because of MetaPost elements' variable names cannot contain any
numbers. Therefore, when e.g. a class name contains numbers one of the
two later variants must be used to define legal variable for element.

Layout
======

Layout part is distinguished from definition part using a line with
three or more ``-``. The layout part is actually just MetaPost, but
some helpful macros and attributes are provided to help placing
elements. Also pure MetaPost is allowed.

horizontally
------------

.. UML:: elements-layout-horizontally

   class foo
   class bar
   ---
   horizontally(50, horiz, foo, bar);

Syntax::

   class foo
   class bar
   ---
   horizontally(50, horiz, foo, bar);

The first parameter ("50") the for space between objects.
The second parameter("horiz") is variable name for the layout's
coordinate system.

vertically
----------

.. UML:: elements-layout-vertically

   class foo
   class bar
   ---
   vertically(50, vert, foo, bar);

Syntax::

   class foo
   class bar
   ---
   vertically(50, vert, foo, bar);

Mixed use
---------

.. UML:: elements-layout-mixed

   class foo
   class bar
   class foobar
   ---
   horizontally(50, horiz, foo, bar);
   vertically(50, vert, horiz, foobar);

Syntax::

   class foo
   class bar
   class foobar
   ---
   horizontally(50, horiz, foo, bar);
   vertically(50, vert, horiz, foobar);

Elements
========

class
-----

.. UML:: elements-class

   class foo

   class bar "abstract"
	fields
		field1
		field2
		fieldn
	methods
		method1
		method2
		methodn
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo

   class bar "abstract"
	fields
		field1
		field2
		fieldn
	methods
		method1
		method2
		methodn
   ---
   horizontally(50, hor_c, foo, bar);

Note: a class' name may contain a stereotype like "abstract" within
quotation marks.

component
---------

.. UML:: elements-component

   component foo

Syntax::

   component foo


interface
---------

.. UML:: elements-interface

   component foo
	assoc foobarA
	assoc foobarB
   foobarA = interface bar1
   foobarB = interface bar2
   ---
   horizontally(50, horiz, foobarA, foobarB);
   vertically(25, vert, horiz, foo);

Syntax::

   component foo
	assoc foobarA
	assoc foobarB
   foobarA = interface bar1
   foobarB = interface bar2
   ---
   horizontally(50, horiz, foobarA, foobarB);
   vertically(20, vert, horiz, foo);

package
-------

.. UML:: elements-package

   package foobar

Syntax::

   package foobar


bigpackage
----------

.. UML:: elements-bigpackage

   bigpackage foobar
	class foo
	class bar
   ---
   horizontally(50, horiz, foo, bar);

Syntax::

   bigpackage foobar
	class foo
	class bar
   ---
   horizontally(50, horiz, foo, bar);

Note: The first syntax of ``bigpackage`` seem to have currently 
a few unfortunate restrictions:

 - ``bigpackage`` itself cannot be linked
 - bigpackages cannot be placed using ``horizontally`` or ``vertically`` macro

.. UML:: elements-bigpackage-explicit

   bigpackage foobar
   class foo
   class bar
   ---
   foo.sw = (50,25);
   horizontally(50, horiz, foo, bar);	
   foobar.sw = (0, 0);
   foobar.ne = (200,75);

Syntax::

   bigpackage foobar
   class foo
   class bar
   ---
   foo.sw = (50,25);
   horizontally(50, horiz, foo, bar);	
   foobar.sw = (0, 0);
   foobar.ne = (200,75);

Connections
===========

inherit
-------

.. UML:: elements-inherit

   class foo
	inherit bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	inherit bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

realize
-------

.. UML:: elements-realize

   class foo
	realize bar
   class bar "abstract"
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	abstract bar
   class bar "abstract"
   ---
   horizontally(50, hor_c, foo, bar);

dep
---

.. UML:: elements-dep

   class foo
	dep "create" bar
   class bar
   ---
   horizontally(100, hor_c, foo, bar);

Syntax::

   class foo
	dep "create" bar 
   class bar
   ---
   horizontally(100, hor_c, foo, bar);

Note: stereotype within quotation marks is obligatory.

use
---

.. UML:: elements-use

   class foo
	use bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	use bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

assoc
-----

.. UML:: elements-assoc

   class (fooA) foo1 
	assoc barA
   class (fooB) foo2
	assoc multi(1) - multi(0..1) barB
   class (fooC) foo3
	assoc aggreg multi(0..1) - multi(*) role(part-of) barC
   class (fooD) foo4
	assoc compos multi(0..1) - multi(*) role(part-of) barD
   class (barA) bar1
   class (barB) bar2
   class (barC) bar3
   class (barD) bar4
   ---
   horizontally(150, hor_cA, fooA, barA);
   horizontally(150, hor_cB, fooB, barB);
   horizontally(150, hor_cC, fooC, barC);
   horizontally(150, hor_cD, fooD, barD);
   vertically(50, ver_c, fooA, fooB, fooC, fooD);

Syntax::

   class (fooA) foo1 
	assoc barA
   class (fooB) foo2
	assoc multi(1) - multi(0..1) barB
   class (fooC) foo3
	assoc aggreg multi(0..1) - multi(*) role(part-of) barC
   class (fooD) foo4
	assoc compos multi(0..1) - multi(*) role(part-of) barD
   class (barA) bar1
   class (barB) bar2
   class (barC) bar3
   class (barD) bar4
   ---
   horizontally(150, hor_cA, fooA, barA);
   horizontally(150, hor_cB, fooB, barB);
   horizontally(150, hor_cC, fooC, barC);
   horizontally(150, hor_cD, fooD, barD);
   vertically(50, ver_c, fooA, fooB, fooC, fooD);

naryassoc
---------

.. UML:: elements-nary

   naryassoc nary
   class (fooA) foo1 
	assoc multi(1) - nary
   class (barA) bar1
	assoc multi(*) - nary
   class (barB) bar2
	assoc multi(*) - nary
   ---
   horizontally(150, hor_c, fooA, nary, barA);
   vertically(50, ver_c, barA, barB);

Syntax::

   naryassoc nary
   class (fooA) foo1 
	assoc multi(1) - nary
   class (barA) bar1
	assoc multi(*) - nary
   class (barB) bar2
	assoc multi(*) - nary
   ---
   horizontally(150, hor_c, fooA, nary, barA);
   vertically(50, ver_c, barA, barB);

qual
----

.. UML:: elements-qual

   class foo
   qual q
	fields
		foobar
	assoc multi(*) - multi(0..1) bar	
   class bar
   ---
   horizontally(150, hor_c, foo, bar);
   q.w = foo.e;

Syntax::

   class foo 
   qual q
	fields
		foobar
	assoc multi(*) - multi(0..1) bar	
   class bar
   ---
   horizontally(150, hor_c, foo, bar);
   q.w = foo.e;

Note: unfortunately, qualifier must be attached manually (see the line ``q.w = foo.e;``).

supply
------

.. UML:: elements-supply

   class foo
	supply bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	supply bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

seqobject
---------

.. UML:: elements-seqobject

   seqobject foo
   seqobject bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   seqobject foo
   seqobject bar
   ---
   horizontally(50, hor_c, foo, bar);

sequence
--------

.. UML:: elements-sequence

   seqobject foo
   seqobject bar

   sequence foobar
   	call foo
		call bar "foobar"
			return
		return
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   seqobject foo
   seqobject bar

   sequence foobar
   	call foo
		call bar "foobar"
			return
		return
   ---
   horizontally(50, hor_c, foo, bar);


Linking
=======

regular
-------

.. UML:: syntax-linking

   page (syntax) "Navidoc UML syntax"
   	link
		syntax.gen.html

Syntax::

   page (syntax) "Navidoc UML syntax"
   	link
		syntax.gen.html

from module
-----------

Syntax::

   page bar
   	link foobar
		bar.html


Note: available modules must be specified in config.

from javadoc
------------

Syntax a)

::

   class org.foobar.foo
	jlink

Syntax b)

::

   class foo
	jlink
		org.foobar.foo

Syntax c)

::

   jlinkpackage org.foobar
   class foo
	jlink

Note: available javadocs must be specified in config.

from doc++
----------

Syntax a)

::

   class foobar::foo
	clink

Syntax b)

::

   class foo
	clink
		foobar

Syntax c)

::

   jlinkpackage foobar
   class foo
	clink

Note: available doc++ documentations must be specified in config.
