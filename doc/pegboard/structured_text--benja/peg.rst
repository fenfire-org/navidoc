======================================================================
``structured_text--benja``: Paragraphs and other text structure in Gzz
======================================================================

:Author:        Benja Fallenstein
:Last-Modified: $Date: 2003/03/31 09:32:00 $
:Revision:      $Revision: 1.1 $
:Type:		Architecture
:Scope:		Major
:Status:        Incomplete
:Date-Created:  2002-12-26


``styled_text--benja`` argues that formatted Xanalogical text
(or other media) should be the primitive in Gzz; however,
the model it defines is not sufficient to compare to modern
formatted text-handling systems like HTML or word processors
like OpenOffice.org Writer.

In particular, we need:

1. Styles applied to individual characters, such as 'emphasis,'
   'code example,' or 'large font.' PEG ``styled_text--benja``
   provides for this.
2. Text structuring into paragraphs, sections with headings,
   tables, bulleted lists, figures, indented blocks, blocks
   outset from the main text flow, and similar constructs,
   all of which can be modified by styles.
   The present PEG proposes a sufficient model.
3. Inline inclusion of structured, non-textual objects into paragraphs,
   such as mathematical formulae, images (possibly glyph-sized),
   ZZ cells shown by a cell view, or 'fields' (textual areas
   whose content is computed). This will be the subject
   of a future PEG.

We will only consider strictly linear models of text; sidebars,
floating images, footnotes or page headers are not provided for.
These are better catered for by external
zzstructural mechanisms and/or Xanalogical linking.
Our enfilade objects are supposed to be better Strings,
that is, objects providing for formatting and Xanalogical media
but not otherwise different from ``String`` objects
(strictly linear in nature).

The structured text system proposed by this PEG does not need
extensions to data model (unlike ``styled_text--benja``,
which required storage of styles along with spans).
Most structural elements can be represented in the model
of ``styled_text--benja``; figures and tables need
the as yet unspecified method for including non-textual objects.
However, new lookup methods to find paragraph boundaries efficiently
are added to enfilade objects.

This PEG is very long, but consists mainly of discussion.
The specification is summarized in the first section.

.. contents::


-------------
Specification
-------------

Representation of paragraphs:

- Paragraphs will be separated by Unicode PS characters (U+2029).
- Paragraph styles on PS characters will apply to the paragraph
  preceding the PS character.
- Paragraph styles on non-PS characters will be ignored.

- If an enfilade ends in a PS character, applications
  will not allow the cursor to move beyond it.
- When a style is to be applied to a paragraph
  that ends with the end of the enfilade, not with a PS character,
  applications will insert a PS at the end of the enfilade.
- When an empty paragraph is to be created at the end of an enfilade
  not ending in a PS character, the application will insert *two*
  PS characters at the end of the enfilade.

- Sections are represented implicitly by applying heading styles
  of different levels to some paragraphs.

- There are styles for bulleted list items at different levels.
- There is a style for paragraphs that aren't list items themselves,
  but belong to the preceding list item.
- When a numbered list is created, an own style for its list items
  is created. Only items of the same style count in the numbering.

- Boxes set out from the rest of the text (such as notes, warnings,
  blockquotes with a line at the left side etc.) also get an own style
  when created, and only paragraphs with the same style are joined
  into a single box.

- Tables are handled by creating an own paragraph for them,
  and inserting the table by the general inclusion mechanism
  for structured data.
- Figures are handled the same way.
  


----------
Discussion
----------

Requirement: Linear model
=========================

As we use a ``String``-like linear model, all enfilades
continue to have ``sub`` and ``plus`` methods.
In order to work like Strings, the following properties
must hold on formatted enfilade objects, where ``e``,
``f``, ``g`` are enfilades, ``m`` and ``n`` are indices
in the enfilades, ``+`` is concatenation, and ``e[m:n]``
is the subenfilade starting at ``m`` and ending before ``n``
(Python slicing syntax)::

    e == e[:m] + e[m:n] + e[n:]
    f == (e + f + g)[len(e) : len(e)+len(f)]
    
(Note that this is somewhat loosely defined, since
we don't define e.g. ``==``. Treat ``e == f``
as, "after all spans in them have been joined,
all lookups on ``e`` and ``f`` return equal results.")

The point is that if you split enfilades and re-join
them, or if you join enfilades and then split them again,
you can get back what you started with. This is not
a trivial statement when dealing with formatted text;
for example, it means that a non-emphasized phrase
inserted inside an emphasized phrase will not change
its styling (if the application desires this,
it has to do it itself). Also, for example in 
OpenOffice.org Writer, cutting a list item,
inserting it somewhere else, cutting it again,
and inserting it in the original context may not
yield the original document. In our system, as long
as no other changes are made to the enfilades, 
it always will.

This provides guarantees of consistency
to the application programmer. It implies that
splitting at any point in the enfilade must result
in reasonable results that can be displayed
(splitting must not bring the enfilade
into an illegal state, as for example
naive splitting of HTML could).


Representing paragraphs
=======================

I have argued earlier that handling paragraphs
through a system outside enfilades may be preferable;
each enfilade would then contain at most one paragraph,
while different paragraphs would be stored
in different zzstructure cells.

However, I've changed my mind: If we're serious
about the ``gzz.media`` API to be independent of zzstructure,
we need to provide an object that can handle paragraphs.
(We *should* provide as much as we can, 
given the linerarity constraints, above.)

Therefore, while it may be beneficial to create bindings
that ensure each paragraph is stored in its own cell,
using the containment mechanism, paragraphs should still
be representable in enfilade objects.

There are two common ways to represent paragraphs
in modern systems: either by markup denoting the beginning
and end of paragraphs (e.g. HTML) or by inserting
a newline character between the paragraphs (e.g. MS Word).
The first isn't really an option for us, since we don't
do interval markup (only markup of individual characters,
possibly using intervals as an internal representation).
The second has the problem that we also need a way
to represent a line break that does not end a paragraph,
for example in computer code or verses. (In an ugly twist,
MS Word uses vertical tabs for this.)

Fortunately, Unicode Standard Annex #13, `Unicode
Newline Guidelines`__, provides a standard way
to deal with precisely this problem, providing
Line Separator (LS) and Paragraph Separator (PS) characters
(U+2028 and U+2029, respectively). We will use
PS to indicate the end of one and beginning of another paragraph.
UAX #13 is part of the Unicode standard.

__ http://www.unicode.org/unicode/reports/tr13/

This implies that paragraph separators are treated
just like ordinary characters by the enfilade.
Concatenating enfilades containing paragraph separators
will have effects similar to concatenating strings
containing newlines.

We will treat newline characters as line separators,
as this seems the 'safer' way; it seems like in 0.6,
users generally used a double-newline to delimit paragraphs,
so we'll provide a converter (probably as a menu item)
that will replace all double newlines in a cell by PS characters.

UAX #13 recommends that PS and LS should be used
whenever the indended function is unambiguous; therefore,
applications (like Gzz bindings) should insert LS rather than
newline characters when they want a line break.

All of the above applies to non-formatted enfilades as well.


Paragraph styling
=================

Supporting styling of paragraphs is essential, since
properties like justification can only be sanely specified
at this level, not at the level of individual characters.
Additionally, formatted text systems traditionally support
specification of character attributes in paragraph styles,
so that all text inside a heading paragraph is in bold,
for example. This seems much more convenient than
requiring the application to maintain a character style
applied to every character in a paragraph.

We will designate certain styles as paragraph style,
as opposed to character styles. This distinction
will not be made at the enfilade level, but in the component
that interprets the styles. All paragraph styles
applied to characters other than PS will be ignored.

A paragraph style applied to a PS character will be interpreted
as applying to the paragraph preceding the PS. This choice
is arbitrary, but familiar from newlines (a newline is considered
part of the line it concludes, not the line it starts).
Both choices lead to unintended results by themselves--

- when inserting a body paragraph with its paragraph mark
  at the beginning of a heading paragraph, the heading
  should stay a heading and the body paragraph
  a body paragraph; and
- when inserting a body paragraph at the end
  of a heading paragraph, the heading should also stay
  a heading and the body paragraph a body paragraph

-- so work from the application is required in either case.
By sticking to the familiar semantics, programmers are likely
to do the correct thing automatically (even though you *could*,
you probably won't insert ``\nfoo`` before a ``\n``--
you'll insert ``foo\n`` after).

Indented text is trivially handled by enabling paragraph styles
to specify an indentation level (like they specify justification etc.).


The last paragraph
==================

The above scheme does not allow applying styles to
the last paragraph in an enfilade, since there is no PS character
after it. This is fixed by requiring an additional PS at the end
if a style is to be applied to the last paragraph.
Applications must not allow the cursor to move beyond a PS
at the very end of an enfilade; if an empty paragraph
at the end of an enfilade is desired, two consecutive PS characters
must be used.

We cannot require a PS at the end of every Gzz cell because
of the containment mechanism: through containment, a cell may be
part of a paragraph inside another cell. In this case,
the cell content isn't a paragraph in itself, but only
a fragment from inside a paragraph. To keep simple things simple,
the interpreted content of a cell should simply be the concatenation
of the "real" cell contents (enfilades) contained in that cell.
Besides, it seems sensible not to declare a cell's content
a paragraph when the intention is for this content to be used
inside another paragraph.

When an application wants to apply a paragraph style
to the last (possibly only) paragraph in a cell,
it must insert a PS at the end. This means that if we apply
a paragraph style to a thing that we don't really consider
a paragraph, we cause the computer to interpret it as a paragraph.
This may be unintended at times, but it seems reasonable.


Sections
========

Many people prefer sections to be defined structurally,
so that e.g. in `XHTML 2.0`_ we have::

    <section>
      <h>Section 1</h>

      <p>Bla bla.</p>

      <section>
        <h>Subsection 1.1</h>

        <p>Text in subsection</p>
      </section>
    </section>

However, this model does not deal easily with splitting
and joining at arbitrary positions. What does the subenfilade
starting at 'bla.' above and ending at the 'x' in 'Text'
look like? If we split at an arbitrary point and then
join again, how do we make sure we get the same enfilade
we started with?

.. _XHTML 2.0: http://www.w3.org/TR/xhtml2/

Things get much easier when we simply designate some paragraphs
as headings and then make a section start at a heading
and end at a heading of the same or a higher level.
This is more like classic HTML::

    <h1>Section 1</h1>

    <p>Bla bla.</p>

    <h2>Subsection 1.1</h2>

    <p>Text in subsection</p>

Since we have already defined splitting styled paragraphs,
splitting at arbitrary points is now well-defined and
joining the resulting enfilades gives us exactly
what we've had before. Additionally, rearrangement
works nicely; for example, if we exchange 
the last two paragraphs, we get the equivalent of ::

    <h1>Section 1</h1>

    <p>Bla bla.</p>

    <p>Text in subsection</p>

    <h2>Subsection 1.1</h2>

which probably matches our intent.


Lists
=====

Word processors frequently handle list items as paragraphs
with a certain style applied to them. This is problematic,
because it does not allow for a list item to contain
more than one paragraph.

However, this can be fixed in a way similar to our handling
of sections, above. We can represent multi-paragraph
bulleted lists by introducing a 'list item continuation'
paragraph style. Such a paragraph will be considered
part of the preceding list item.

This does not suffice for numbered lists, because we need
to know which items belong to the same list and where
a new list starts. This can be solved by creating
a new style when a new list is created, and count
only paragraphs with that style when generating
the number for any given list item. Potentially, this allows
non-list paragraphs to be inserted inside the list, like this:

    The items are,

        1. The first item.

    This is included because of this and that.

        2. The second item.

    This is included because of that and this.


Boxes
=====

Often we want to make a box containing one or more paragraphs
standing out from the main text, for example containing
a side note or warning. Block quotes rendered with a line
at the left side, as have become popular in email clients
recently, are another example.

It does not suffice to simply have 'note' and 'warning' styles
that can be applied to paragraphs, because then we could not
distinguish between two paragraphs belonging to the same note,
and two different notes one after another.

We handle this the same way as numbered lists: when a box
is created, it gets its own style, and two consecutive
paragraphs are only shown in the same box if they're
of the same style. This is particularly useful with
block quotes, where you can rearrange arbitrarily,
yet have two consecutive paragraphs from the same source joined,
but not two consecutive paragraphs from different sources.


Tables
======

Tables are not linear, so we make no attempt at representing
them linearly-- a table is a single unit in an enfilade,
you can only have all or none of it. This is in keeping
with common word processors, which, when striping text,
only allow you to select a table as a whole.

Tables will be defined by the standard mechanism
to include non-textual structured data (yet to be defined).
We will create an own paragraph for the table
and insert it there.

Of course this is only for tables we want to have in the
text flow (as in "This table shows all tags:" followed
by a table of the HTML tags in the next paragraph).
Another way to refer to tables is through a Xanalogical link,
which will usually show the table floating in the margin.


Figures
=======

Figures are handled like tables. If a figure has a caption,
that may be a paragraph with an appropriate style,
above or below the figure itself.


\- Benja