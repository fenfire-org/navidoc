/*
RefValueMap.java
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

/** A map where the <em>values</em> are referred to by soft/weak/phantom references -- useful for
 * caches.
 * This is an abstract base class to which the derived implementations add the 
 * reference creating method.
 * <p>
 * There is room for optimization: implementing the hash really in this class instead
 * of using the HashMap delegation would result in one less object per entry.
 * <p>
 * NOTE: This class does not currently implement all of the Map interface - some methods
 * throw an UnsupportedOperationException. This should be fixed at some point.
 */
public abstract class RefValueMap implements Map {

    private HashMap map = new HashMap();
    protected ReferenceQueue queue = new ReferenceQueue();

// These two are implemented as defined in the javadoc.

    /** Implement hashcode for map.entries.
     * This is for use by subclasses which have their 
     * classes extending Soft/Weak/Phantom Reference and Map.Entry.
     */
    protected static int hashCode(Map.Entry e) {
	Object val = e.getValue(); // atomic -- getValue() result may change by GC thread
	return
	     (e.getKey()==null   ? 0 : e.getKey().hashCode()) ^
	      (val==null ? 0 : val.hashCode()); 
    }
    /** Implement equals for map.entries.
     * This is for use by subclasses which have their 
     * classes extending Soft/Weak/Phantom Reference and Map.Entry.
     */
    protected static boolean equals(Map.Entry e1, Map.Entry e2) {
	Object e1val = e1.getValue(); // atomic -- see above
	Object e2val = e2.getValue();
	return 
	 (e1.getKey()==null ?
	  e2.getKey()==null : e1.getKey().equals(e2.getKey()))  &&
	 (e1val==null ?
	  e2val==null : e1val.equals(e2val));
    }

    protected abstract Object makeValue(Object key, Object value, ReferenceQueue queue);


    protected void clean() {
	Map.Entry o;
	while((o = (Map.Entry)queue.poll()) != null)
	    map.remove(o.getKey());
    }

    public Object put(Object key, Object value) {
	clean();
	Map.Entry ret = (Map.Entry)map.put(key, makeValue(key, value, queue));
	if(ret == null) return null;
	return ret.getValue();
    }

    private Set entrySet = new AbstractSet() {
	Set set = map.entrySet();
	public Iterator iterator() {
	    final Iterator iter = set.iterator();
	    return new Iterator() {
		public boolean hasNext() { 
		    return iter.hasNext();
		}
		public Object next() {
		    // Get our Value object
		    return ((Map.Entry)(iter.next())).getValue();
		}
		public void remove() {
		    iter.remove();
		}
	    };
	}
	public int size() {
	    return map.entrySet().size();
	}
	public boolean add() {
	    throw new UnsupportedOperationException();
	}
    };

    public Set entrySet() {
	clean();
	return entrySet;
    }

// --- Explicitly delegate to map.

    public Object remove(Object key) {
	Map.Entry entry =  (Map.Entry)map.remove(key);
	if(entry == null) return null;
	return entry.getValue();
    }

    public Object get(Object key) {
	Map.Entry entry = (Map.Entry)map.get(key);
	if(entry == null) return null;
	return entry.getValue();
    }

    public Set keySet() {
	return map.keySet();
    }


    public void putAll(Map m) {
	for(Iterator i = m.entrySet().iterator(); i.hasNext();) {
	    Map.Entry entry = (Map.Entry)i.next();
	    put(entry.getKey(), entry.getValue());
	}
    }
    public boolean containsKey(Object key) {
	return map.containsKey(key);
    }
    public boolean isEmpty() {
	return map.isEmpty();
    }
    public void clear() {
	map.clear();
    }
    public int size() {
	return map.size();
    }

    public Collection values() {
	throw new UnsupportedOperationException();
    }
    public boolean containsValue(Object value) {
	throw new UnsupportedOperationException();
    }


}

