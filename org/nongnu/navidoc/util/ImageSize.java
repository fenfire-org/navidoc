/*
ImageSize.java
 *    
 *    Copyright (c) 2003, : Tuomas J. Lukka
 *    
 *    This file is part of Gzz.
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
 * Written by : Tuomas J. Lukka
 */

package org.nongnu.navidoc.util;
import java.io.*;
import java.awt.Dimension;

/** Methods for determining sizes of image files.
 * Initially, only PNG is supported.
 */
public class ImageSize {

    private static int ub(byte b) {
	if(b < 0) return b + 256;
	return b;
    }

    /** Big-endian long.
     */
    private static int belong(byte[] b) {
	return ub(b[0]) * 256 * 256 * 256 +
	       ub(b[1]) * 256 * 256 +
	       ub(b[2]) * 256 +
	       ub(b[3]);
    }

    /** Read the size of an image file.
     */
    static public Dimension readSize(File f) {
	try {
	    FileInputStream is = new FileInputStream(f);
	    return readSize(is);
	} catch(IOException e) {
	    return null;
	}
    }

    /** Read the size of an image given an inputstream.
     */
    static public Dimension readSize(InputStream is) {
	try {
	    byte[] in = new byte[4];
	    is.read(in);
	    if(ub(in[0]) == 0x89 &&
		ub(in[1]) == 'P' &&
		ub(in[2]) == 'N' &&
		ub(in[3]) == 'G' 
		) {
		// It's PNG. We know this.
		is.skip(12);
		is.read(in);
		int width = belong(in);
		is.read(in);
		int height = belong(in);
		return new Dimension(width, height);
	    }
	    return null;

	} catch(IOException e) {
	    return null;
	}
    }
}
