=============================================================
PEG tests_output_cleanup--vegai: Cleaning Tests' Output
=============================================================

:Author:   Vesa Kaihlavirta
:Last-Modified: $Date: 2003/03/31 09:32:00 $
:Revision: $Revision: 1.1 $
:Status:   Incomplete
:Scope:	   Minor
:Type:     Policy?


Our tests' output is seriously cluttered. This PEG will propose standards
that, when implemented, will result in clean test output.

Clean test output includes the test docstring -- which should take only one
line -- and the result ("ok", or "fail" and traceback, or a reason why the
test wasn't run).

Issues
======

- There needs to be a way to get extra debug information from a failing test.
  How do we turn that on? What code inside the test?


Problems and solutions
======================

Listing individual problems from current (2003/01/09) test output.


1. When test cost is considered, output is bizarre::

    TEST COST  <function testStarts at 2220309> 10
    TOO COSTLY TEST <function testStarts at 2220309>

    Solution: new format for test output, test shouldn't print anything extra::

        [test method docstring] ... skipping (cost too high: 10).
 

2. Garbage when initalizing test.gfx::

    Init test.gfx
    ['__doc__', '__file__', '__name__', '__path__', 'client', 'fuzzy', 'gfx',
    'impl', 'media', 'util', 'vob']
    ['GraphicsAPI', '__doc__', '__file__', '__name__', '__path__']
    Jan 9, 2003 2:09:05 AM java.util.prefs.FileSystemPreferences$3 run
    WARNING: Could not create system preferences directory. System preferences
    are unusable.
    GW:  gzz.client.awt.FrameScreen@85097d

    Solution:
    
        - Fix init.gfx, it presumably outputs excess debug

  
3. gzz/media/impl/PageImageScroll.java has pa()::

    Checked document of 0 pages

    Solution: fix method, debug information


4. Bizarre error again, not unlike 1.::

    TEST FAILS IN  <function testStripBlock at 4952321> *
    NOT RUNNING DUE TO WRONG F:  <function testStripBlock at 4952321>

    Solution: clarify or remove "NOT RUNNING DUE TO WRONG F:".


5. test/tools/gfx.py outputs "CBCF init".

   Solution: as in 3.


6. Some of the tests output debug information, eg::

    Test space saving and re-loading ... []
    [[[01F3F91514A6E80BCDFD6D978DACD0C40B4999DAF1]],
    [[019FA251833B0791D550BE3D03EC67234BAACDADC1]],
    [[01709BC0FC0687E569572437F562456C6D24FEC7FB]]]
    [[[01F3F91514A6E80BCDFD6D978DACD0C40B4999DAF1]],
    [[019FA251833B0791D550BE3D03EC67234BAACDADC1]],
    [[01709BC0FC0687E569572437F562456C6D24FEC7FB]]]
    [[[01F3F91514A6E80BCDFD6D978DACD0C40B4999DAF1]],
    [[019FA251833B0791D550BE3D03EC67234BAACDADC1]],
    [[01709BC0FC0687E569572437F562456C6D24FEC7FB]]]
    [[[01F3F91514A6E80BCDFD6D978DACD0C40B4999DAF1]],
    [[019FA251833B0791D550BE3D03EC67234BAACDADC1]],
    [[01709BC0FC0687E569572437F562456C6D24FEC7FB]]]
    SliceVersion([SliceVersion.Conn('urn:urn-5:7ZnIxDowCCU4ozTsf6oE45zIRTId:2',
    'urn:urn-5:7ZnIxDowCCU4ozTsf6oE45zIRTId:1',
    'urn:urn-5:7ZnIxDowCCU4ozTsf6oE45zIRTId:3')],
    {urn:urn-5:7ZnIxDowCCU4ozTsf6oE45zIRTId:1=Enf1DImpl[null,SPAN1D(gzz.media.impl.TransientTextScroll@1e12e2c
    0 3),null]})
    ... (goes on and on)

    Solution: Fix test, debug information.

7. gzz/impl/mirror/MasterImpl.java outputs "Sending change:".

    Solution: As in 5.

8. Enfilades' test spurts weird things::

    Test enfilades consisting of no spans and a single span. ... Jan 9, 2003
    2:09:36 AM java.util.prefs.FileSystemPreferences checkLockFile0ErrorCode
    WARNING: Could not lock System prefs.Unix error code 134984164. 
    Jan 9, 2003 2:09:36 AM java.util.prefs.FileSystemPreferences syncWorld
    Jan 9, 2003 2:09:36 AM java.util.prefs.FileSystemPreferences syncWorld
    WARNING: Couldn't flush system prefs: java.util.prefs.BackingStoreException:
    Couldn't get file lock.

    Solution: No idea currently. Something is outputting debug info again excessivly.

9. SolidBGVob test outputs debug information, and the same problem as in
   8.::

    testSingle_solidbgvob (__main__.Boxcellview) ... Jan 9, 2003 2:10:06 AM
    java.util.prefs.Fi
    leSystemPreferences checkLockFile0ErrorCode
    WARNING: Could not lock System prefs.Unix error code 134984164.
    Jan 9, 2003 2:10:06 AM java.util.prefs.FileSystemPreferences syncWorld
    WARNING: Couldn't flush system prefs: java.util.prefs.BackingStoreException:
    Couldn't get
    file lock.
    ok
    testSingleNote (__main__.Coordinateplane) ... CBCF init
    New note

    PLace
    CPV: 'urn:urn-5:nbYfgs3K6YzPEUPJJ7vfLutFDZta:1' (Uusi paperi) null
    CPV STEP: 'urn:urn-5:nbYfgs3K6YzPEUPJJ7vfLutFDZta:2' (FOO)
    'urn:urn-5:nbYfgs3K6YzPEUPJJ7vf
    LutFDZta:1' (Uusi paperi)
    CPV: 'urn:urn-5:nbYfgs3K6YzPEUPJJ7vfLutFDZta:2' (FOO)
    'urn:urn-5:nbYfgs3K6YzPEUPJJ7vfLutFD
    Zta:3' (100)
    CBCF getsize ('urn:urn-5:nbYfgs3K6YzPEUPJJ7vfLutFDZta:2' (FOO),
    gzz.view.AbstractViewConte
    xt@1349665, array([50.0, 50.0], float))
    CPV PLACE: 100 200 50.0 50.0
    Place:  1
    CPV STEP: null 'urn:urn-5:nbYfgs3K6YzPEUPJJ7vfLutFDZta:1' (Uusi paperi)
    Placed
    ok

    Solution: As in 7. and 8.


Alternative Solution
====================

Find a way to disable output during the tests.

