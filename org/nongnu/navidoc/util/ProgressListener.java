/*   
ProgressListener.java
 *    
 *    Copyright (c) 2005, Matti J. Katila
 *                  2005, Benja Fallenstein
 *
 *    This file is part of Navidoc.
 *    
 *    Fenfire is free software; you can redistribute it and/or modify it under
 *    the terms of the GNU General Public License as published by
 *    the Free Software Foundation; either version 2 of the License, or
 *    (at your option) any later version.
 *    
 *    Fenfire is distributed in the hope that it will be useful, but WITHOUT
 *    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 *    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
 *    Public License for more details.
 *    
 *    You should have received a copy of the GNU General
 *    Public License along with Fenfire; if not, write to the Free
 *    Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
 *    MA  02111-1307  USA
 *    
 *
 */
/*
 * Written by Matti J. Katila and Benja Fallenstein
 */

package org.nongnu.navidoc.util;

/** An callback interface for progress meter used in 
 *  some of the sub projects of Fenfire.
 */
public interface ProgressListener {

    /** Something between 0 and 1.
     */
    void setProgress(float progress);
    void setMessage(String whatIsGoingOn);
}
