/*
WeakValueMap.java
 *    
 *    Copyright (c) 2003, : Tuomas J. Lukka
 *    
 *    This file is part of Libvob.
 *    
 *    Libvob is free software; you can redistribute it and/or modify it under
 *    the terms of the GNU General Public License as published by
 *    the Free Software Foundation; either version 2 of the License, or
 *    (at your option) any later version.
 *    
 *    Libvob is distributed in the hope that it will be useful, but WITHOUT
 *    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 *    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
 *    Public License for more details.
 *    
 *    You should have received a copy of the GNU General
 *    Public License along with Libvob; if not, write to the Free
 *    Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
 *    MA  02111-1307  USA
 *    
 *    
 */
/*
 * Written by : Tuomas J. Lukka
 */

package org.nongnu.navidoc.util;
import java.util.*;
import java.lang.ref.*;

/** A map where the <em>values</em> are referred to by weak references -- useful for
 * some types of caches.
 * <p>
 * The JDK should really provide this...
 */
public class WeakValueMap extends RefValueMap {

    private static class Value extends WeakReference implements Map.Entry{
	private Object k;
	Value(Object k, Object v, ReferenceQueue queue) {
	    super(v, queue);
	    this.k = k;
	}
	public Object getKey() { return k; }
	public Object getValue() { return get(); }
	public Object setValue(Object o) {
	    throw new UnsupportedOperationException();
	}


	public int hashCode() { 
	    return RefValueMap.hashCode(this);
	}
	public boolean equals(Object o) {
	    return RefValueMap.equals(this, (Map.Entry)o);
	}

    }

    protected Object makeValue(Object k, Object v, ReferenceQueue queue) {
	return new Value(k, v, queue);
    }

}

