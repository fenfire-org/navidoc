/*
ObsTrigger.java
 *    
 *    Copyright (c) 1999-2001, Ted Nelson and Tuomas Lukka
 *
 *    This file is part of Navidoc.
 *    
 *    Gzz is free software; you can redistribute it and/or modify it under
 *    the terms of the GNU General Public License as published by
 *    the Free Software Foundation; either version 2 of the License, or
 *    (at your option) any later version.
 *    
 *    Gzz is distributed in the hope that it will be useful, but WITHOUT
 *    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 *    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
 *    Public License for more details.
 *    
 *    You should have received a copy of the GNU General
 *    Public License along with Gzz; if not, write to the Free
 *    Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
 *    MA  02111-1307  USA
 *    
 *
 */
/*
 * Written by Tuomas Lukka
 */

package org.nongnu.navidoc.util;

/** An interface for attaching and triggering Obses.
 * Basically, each observer (Obs) may observe several 
 * combinations of (Object, Object) pairs. The first one of the objects is
 * expected to have '==' equality, generally they will be Dims or objects
 * inside dims.
 * The second object is used through .equals.
 * <p>
 * This interface is meant for synchronous use: 
 * the Obs.chg() methods are called 
 * only from the callQueued method of this class.
 * <p>
 * This is mostly meant to be used <i>inside</i> space
 * implementations.
 * @see Obs
 */
public interface ObsTrigger {


    /** Add an observer.
     *  @param o The observer. If <code>null</code>, nothing is done;
     *           no error may be thrown. (Rationale: otherwise, we
     *           would have to check for nullity in all places that
     *           call <code>addObs</code>, because they can
     *           (almost) <em>all</em> be passed <code>null</code>
     *           observers.)
     */
    void addObs(Obs o, Object obj, Object code);

    /** Remove all observations that the given observer is making.
     */
    void rmObs(Obs o);

    /** Signal that the observers for the given pair should
     * be triggered.
     * All observers that are triggered are then removed from
     * further processing.
     */
    void chg(Object obj, Object code);

    /** Call the changed observers.
     */
    void callQueued();

}
