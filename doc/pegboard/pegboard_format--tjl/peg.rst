=============================================================
PEG ``pegboard_format--tjl``: PEG format and process
=============================================================

:Authors:  Tuomas Lukka
:Stakeholders: Asko Soukka
:Last-Modified: $Date: 2003/06/06 20:04:24 $
:Revision: $Revision: 1.3 $
:Status:   Current

This META-PEG deals with formatting PEGs.

Issues
------

    - Our own RST directives?

        RESOLVED: Not yet. Of course, there's UML but that's
	used in other docs. Nothing pegboard-specific.

    - Should we use urn-5 instead of serial numbers to avoid
      collisions? This could be a nice application.

        RESOLVED: Not. Not human-readable enough. Collisions
	are resolved by using the individual user names 
	described below instead of serial numbers.

    - What should we say about the issues section?

	RESOLVED: The issues section should contain all the uncertain
	points of the specification; there should not be questions
	at any other point. Once an issue is resolved, the resolution
	and its rationale should be here.

	Issues should be clear **questions** which need answers.
	"I'm not sure about X." would be much better phrased as
	"Should we do X?". That way there is a clear question,
	to which we are seeking a simple answer.

	Resolutions of issues should always contain reasoning
	behind them::

	    - should we do X?

		RESOLVED: No

	is not good. Should be::

	    - should we do X?

		RESOLVED: No, since that would interfere with Y.

	Even ::

	    - should we do X?

		RESOLVED: No, not yet

	is much better, since it at least gives more information.

	The point is that issues once raised will continue to be raised,
	and having the reply *with the reasons* at hand helps avoid
	getting stuck in loops.

    - Do we need the Scope and Type fields?

	RESOLVED: They don't hurt.

What is a PEG?
--------------

"PEG" used to be short for "Proposal for Enhancing Gzz". At the moment,
it's just PEG, with no real acronym meaning.

At the moment, PEGs are used in all the Gzz-split projects, i.e. Fenfire,
Libvob, CallGL, Alph, Storm, ...

A PEG is a short document detailing, for example,

- An architectural plan for an extension

- Changes to a core interface

- Plans for experiments

- File format specification that is to be used somewhere

- Code style specifications

- User interface specifications

- Roadmaps

I.e. *any* kind of plan or specification that needs to be discussed among the 
group members.  The PEG process is about writing out some plan, submitting
it for peer review among the group, resolving issues raised by the group and
clarifying the relevant parts and finally voting (or dictatorial acceptance by
the project leader) -- i.e. the PEG process is about achieving **consensus**.

PEGs are especially important for the Jyu Hyperstructure Research group because
we're geographically outspread and open, so PEGs are vital for everyone
knowing what the others are thinking about.

PEGs are also an educational instrument for learning to write English text comfortably.

Process
-------

Anyone may start a new PEG in the Incomplete state (becoming
one of the PEG's authors).  The authors have control over the contents of the PEG.
In addition, anyone may enter new issues to a PEG.

When the PEG seems ready for review, it should be made Current and
posted to gzz-dev. At this point, the PEG may still be edited
in response to comments from the list.

As long as the PEG is in Incomplete or Current state, the author
may change its status to Current, Incomplete (for revision),
Irrelevant (e.g., other PEGs superceded the current one) or
Postponed (i.e. while making the PEG it became clear that the time is not yet ripe
for it, something else needs to be done first.). Postponed PEGs may be moved to the other
non-accepted states freely by the author.

**NOTE**: PEGs should not be made Current as long as there are unresolved
issues. If the responses from the list raise issues that cannot be immediately
resolved, the PEG should be put into Incomplete state again.

At some point after this, the project leader (varies for the different subprojects) 
will make a decision
to either accept, force revision, declare rejected, or declare
irrelevant. No-one else may change the status of the PEGs 
to Accepted or Rejected. While it is allowed, the project leader should avoid accepting PEGs
that have not been posted to the mailing list for review in their latest form.

If the PEG was accepted, rejected or declared irrelevant, it may not
be edited any more, except for the architect or author
declaring it implemented or partly implemented from the accepted state.  
For rejected or irrelevant PEGs, new PEGs should be started.

A PEG int the Revising state is editable by the authors, similarly to
an incomplete PEG.



Names
-----

The PEGs are not numbered but named, with names such as::

    move_vobs--benja
    move_vobs_2--benja
    meta_new_fields--tjl

These names are used for the directory names. The last part is the handle of the author, 
to ensure uniqueness.

Inside the directory, there should be one reStructuredText file,
called ``peg.rst`` and any number of other files (images, example code ...).

Overall structure
-----------------

The PEG should begin with the header and after that, a short
introduction which should briefly answer the questions **what** and **why**
(and, if not obvious, **how**).

After this section, there should be an Issues section (following
the example of OpenGL extension specs), which should contain the
open questions related to this PEG. Once an issue is resolved, it
is often good to leave the resolution and the 
rationale behind the resolution into the Issues section

Then, there can be free-form sections in which the changes proposed
are detailed.


Header
------

The Header of the PEG should contain the following fields:

Authors
    Comma-separated list of author names or handles

Date-Created
    The date the PEG was created (or submitted)

Last-Modified
    CVS date tag

Revision
    CVS revision tag

Status
    The PEG status

and may **optionally** also contain the following fields:

Stakeholders
    Comma-separated list of stakeholder names or handles

Scope
    How large the effects of this PEG are:

    Major
	Most code needs a touchup
    Minor
	limited
    Trivial
	few places need to be changed in a trivial way
    Cosmetic
	name changes and the like

Type
    The type of the PEG

    META
	PEG about PEGs
    Policy
	Setting goals, overall ideas; e.g. ``styled_text--benja`` 
    Architecture
	Architectural changes; e.g. ``1005``
    Feature
	A new feature; e.g. ``vobcoorder_isactive--tjl``
    Interface
	An adjustment of one or more interfaces; e.g. ``1017``
    Implementation
	An adjustment of how an implementation does something

Affects-PEGs

    A comma-separated list of the PEGs that this PEG affects: since
    accepted PEGs may not be modified, this field explains which
    PEGs define behaviour that is to be modified by this PEG.

    The idea is that the reST compiler would take this into account
    and mention the affecting PEGs in a compiled PEG.

Low-level Format
----------------

PEGs use the python reStructuredText_ markup language.

.. _reStructuredText: http://docutils.sourceforge.net

Sentences should not begin with either PEG names,
variable names or anything like that. So::

    ``miniblocks--benja`` showed how ...

should be replaced with ::

    The PEG ``miniblocks--benja`` showed how

Or at the very least

    In ``miniblocks--benja`` it was shown how


