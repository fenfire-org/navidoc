==========================================
UML stereotypes for describing Vob structs
==========================================

These UML steretypes are described in LibVob's PEG:
"UML stereotypes for describing Vob structs".

vobin
-----

.. UML:: elements-vobin

   class foo
	vobin - bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	vobin - bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Note: like assoc 

vobtransform
------------

.. UML:: elements-vobtransform

   class foo
	vobtransform - bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	vobtransform - bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Note: like assoc

vobtransformsub
---------------

.. UML:: elements-vobtransformsub

   class foo
	vobtransformsub - bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	vobtransformsub - bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Note: like assoc

vobsubmatch
-----------

.. UML:: elements-vobsubmatch

   class foo
	vobsubmatch bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);

Syntax::

   class foo
	vobsubmatch bar
   class bar
   ---
   horizontally(50, hor_c, foo, bar);
