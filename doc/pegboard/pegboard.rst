===============================
Proposals for enhancing Navidoc
===============================

.. As seen on the mailing lists, we need some structure to new
   architectural ideas. Let's try this.
 
   All changes to the following packages ("frozen" packages)
   and classes **must** go through PEGs:

   * gzz
 
   * gzz.media

   * gzz.diff
    
   * gzz.impl.AbstractSpace

   * gzz.impl.AbstractDim

   * gzz.impl.ModularSpace
 
   * gzz.impl.CellManager

   * gzz.impl.DimManager

   * gzz.impl.IdentityManager
    
   * gzz.vob

   Note, however, that these are not recursive: freezing ``gzz.vob`` 
   does **not** mean that ``gzz.vob.vobs`` would be frozen - that package
   is most definitely not frozen.

   Any other semantic changes to the frozen packages and classes 
   will be **summarily**
   rejected and reverted. If you need a change quickly, then **subclass** 
   or **create a branch**. 
   Changes to javadoc and indentation etc. are exempted, 
   as are bug fixes that correct classes to compliance with javadoc or 
   the architecture documentation in *doc/*.

   This list will be updated once in a while, to reflect newly stabilized packages.
 
   It is also **recommended** that large changes to other classes or 
   packages be PEGged first but not required: such changes will not 
   be summarily rejected. 

PEGs should use the python reStructuredText_ markup language. `Quick reference`__
could be handy.

.. _reStructuredText: http://docutils.sourceforge.net
.. _QuickRef: http://docutils.sourceforge.net/docs/rst/quickref.html

__ QuickRef_

Pegboard
--------

.. pegboard::


Explanation of table:
---------------------
 
Status
    	The current status of the PEG.

	current
		Currently under active consideration for accepting or rejecting.

	revising
		After being rejected, being revised for another round.
	

	incomplete
		Not yet being considered; details still being worked out by 
		author and stakeholders.

	undefined
		Status is not yet defined, or peg's syntax is broken.
	
	accepted
		Accepted for implementing.
	
	implemented
		The changes are currently in main CVS. 
		This PEG is now frozen, no changes should be 
		made to it any more.

	rejected
		Rejected through peer review in the consensus process. 
		Can be revived by being revised.

	irrelevant    
		seems to be superseded by later PEGs.

Topic
    	A brief description of the main purpose of the PEG.

Authors
    	The author(s) (owner[s]) of the PEG; only this person can edit the 
	main text of the PEG.

Stakeholders
	The people who consider this PEG important for their work and 
	need to have their views represented. For instance, users of an 
	API being considered, the designer of the parts that now require 
	changing etc. **Feel free to add yourself if you consider the 
	change important.**

Files
	All files related with PEG.
