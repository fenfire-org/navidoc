# 
# Copyright (c) 2002, 2003 Tuomas Lukka, Asko Soukka
# 
# This file is part of Navidoc.
# 
# Navidoc is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# Navidoc is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General
# Public License along with Navidoc; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
# 

# $Id: parser.py,v 1.3 2003/06/27 13:17:00 humppake Exp $

#
# Written by Tuomas Lukka, Asko Soukka
#

__docformat__ = 'reStructuredText'

import re, random

import navidoc

def match_remove(p, s):
    """
    match_remove(p, s)

    Match pattern p in s and remove the match, return match and the
    rest of the string.).
    """
    m = re.match(p,s)
    if m: s = re.sub(p, "", s)
    return (m, s)

def tabs_to_spaces(s):
    """
    tabs_to_spaces(s)

    Transform tabs into spaces. Return the transformed string.
    """
    return re.sub("\t", "        ", s);

def init_spaces(s, tokenize=0):
    """
    init_spaces(s, tokenize=0)

    Strip whitespaces and calculates the amount of them in the
    beginning of the string. Return the amount and stripped
    string. Stripped string could also be tokenized - using
    whitespace as tokenizer.
    """
    n = len(re.match("^\s*", s).group())
    if tokenize: return (n, s.strip().split())
    else: return (n, s.strip())
def random_var():
    """
    random_var()

    Return a 20 random character string.
    """
    letters = "abcdeghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ"
    l = len(letters)
    return "".join([
	letters[random.randint(0, l-1)] 
	    for k in range(20)])

def parse_indented(s, tokenize=1):
    """
    parse_indented(s, tokenize=1)

    Split the string into lines after "\n"s. Parse the string
    array into array tree after indentions in consecutive strings.
    May also tokenize strings - whitespace as tokenizer.
    Return the parsed array.
    """
    stack = [(-1, [])]
    for r in s.split("\n") :
	if re.match("^\s*$", r): continue
	r = tabs_to_spaces(r) 
        if tokenize: (n,x) = init_spaces(r, tokenize=1)
        else: (n,x) = init_spaces(r)
	while n < stack[-1][0]:
	    stack.pop()
	if n > stack[-1][0]:
	    new = (n, [x])
	    stack[-1][1].append(new[1])
	    stack.append(new)
	else: # x == stack[-1][0]:
	    new = (n, [x])
	    stack[-2][1].append(new[1])
	    stack.pop()
	    stack.append(new)
    return stack[0][1]

def keys_for_classes(module, top_class):
    """
    keys_for_classes(module, top_class)
    
    Gather a key -> class dictionary for all subclasses of top_class
    containing 'key' in the given module. In Navidoc this is used to
    collect UML elements from modules.
    """
    d = {}
    for element in dir(module):
        element = getattr(module, element)
        if type(element) == type(top_class) \
                       and issubclass(element, top_class):
            if hasattr(element, "key") \
                   and type(element.key) == type(''):
                d[element.key] = element
    return d
