/*
CachingMap.java
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

/** A map that has a maximum number of entries at any given time.
 * The put method has a side effect of possibly removing entries
 * from the map, including the just added entry, to keep the size
 * within the limits.
 * Currently removes elements randomly, will use LRU later.
 */
public class CachingMap implements Map {
    private HashMap map = new HashMap();
    private int maxEntries;

    /** An interface for values that need to know when they
     * are removed from the map.
     */
    public interface Removable {
	/** Called when this value was removed (from the given key.
	 */
	void wasRemoved(Object key);
    }

    /** Create a new cachingmap with the given maximum number of entries.
     * @param maxEntries Number of entries to keep. 0 = don't cache anything.
     */
    public CachingMap(int maxEntries) {
	this.maxEntries = maxEntries;
	if(maxEntries < 0) throw new Error("Can't keep so few.");
    }

    public Object put(Object key, Object value) {
	if(maxEntries == 0) return null;

	Object ret = map.put(key, value);
	int toRemove = map.size() - maxEntries;
	while(toRemove-- > 0) {
	    Iterator i = map.keySet().iterator();
	    for(int nth = (int)(Math.random() * map.size()); nth > 0; nth--) {
		i.next();
		if(!i.hasNext()) 
		    i = map.keySet().iterator();
	    }
	    Object rkey = i.next();
	    Object rval = map.get(rkey);
	    if(rval instanceof Removable) 
		((Removable)rval).wasRemoved(rkey);
	    map.remove(rkey);
	}
	return ret;
    }

    public Set entrySet() { return map.entrySet(); }


// --- Explicitly delegate to map.

    public Object remove(Object key) {
	return  map.remove(key);
    }

    public Object get(Object key) {
	return map.get(key);
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
	return map.values();
    }
    public boolean containsValue(Object value) {
	return map.containsValue(value); 
    }


    
}
