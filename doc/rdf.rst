==========================================
RDF elements for describing RDF vocabulary
==========================================

rdf-resource
------------

.. UML:: elements-rdfresource

   rdf-resource foo

Syntax::
 
   rdf-resource foo

rdf-literal
-----------

.. UML:: elements-rdfliteral

   rdf-literal foo

Syntax::
 
   rdf-literal foo


Example
-------

.. UML:: elements-rdfexample

   rdf-resource foobar
      assoc foo
      assoc bar

   rdf-literal foo
   rdf-literal bar
   ---
   horizontally(50, h, foo, bar);
   vertically(50, v, foobar, h);

Syntax::
 
   rdf-resource foobar
      assoc foo
      assoc bar

   rdf-literal foo
   rdf-literal bar
   ---
   horizontally(50, h, foo, bar);
   vertically(50, v, foobar, h);
