% 
% Copyright (c) 2002, 2003 Tuomas Lukka
% 
% This file is part of Navidoc.
% 
% Navidoc is free software; you can redistribute it and/or modify it under
% the terms of the GNU General Public License as published by
% the Free Software Foundation; either version 2 of the License, or
% (at your option) any later version.
% 
% Navidoc is distributed in the hope that it will be useful, but WITHOUT
% ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
% or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
% Public License for more details.
% 
% You should have received a copy of the GNU General
% Public License along with Navidoc; if not, write to the Free
% Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
% MA  02111-1307  USA
% 

% $Id: uml.mp,v 1.16 2003/07/28 14:44:35 humppake Exp $

%
% Written by Tuomas Lukka
%

defaultfont := "Helvetica";

def picmeasurements(suffix b) =
    pair b.size, b.e, b.n, b.w, b.s, b.ne, b.nw, b.se, b.sw, b.c;
    b.size := urcorner(b.pict) - llcorner(b.pict);
    b.e = b.w + ((xpart b.size), 0);
    b.n = b.s + (0, (ypart b.size));
    b.ne = (xpart b.e, ypart b.n);
    b.nw = (xpart b.w, ypart b.n);
    b.se = (xpart b.e, ypart b.s);
    b.sw = (xpart b.w, ypart b.s);
    b.c = 0.5[b.w, b.e];
    b.e = 0.5[b.ne, b.se];
    b.n = 0.5[b.ne, b.nw];
enddef;

def unknownpicmeasurements(suffix b) =
    pair b.size, b.e, b.n, b.w, b.s, b.ne, b.nw, b.se, b.sw, b.c;
    b.e = b.w + ((xpart b.size), 0);
    b.n = b.s + (0, (ypart b.size));
    b.ne = (xpart b.e, ypart b.n);
    b.nw = (xpart b.w, ypart b.n);
    b.se = (xpart b.e, ypart b.s);
    b.sw = (xpart b.w, ypart b.s);
    b.c = 0.5[b.w, b.e];
    b.e = 0.5[b.ne, b.se];
    b.n = 0.5[b.ne, b.nw];
enddef;

def know(expr b) =
    show b;
    if not known b: b = 0; fi;
    show b;
enddef;

def fixmeasuredpic(suffix b) =
    know(xpart b.c);
    know(ypart b.c);
enddef;

def drawmeasuredpic(suffix b) =
    fixmeasuredpic(b);
    addto currentpicture also b.pict shifted (b.ne-urcorner(b.pict));
enddef;

vardef bboxmeasuredpic(suffix a) =
    fixmeasuredpic(a);
    (a.n--a.ne--a.e--a.se--a.s--a.sw--a.w--a.nw--cycle)
enddef;


%%%%%%%%%%%%%%%%%%%
%
%  Fonts etc

def fontHeight(expr f) =
begingroup
    save pict;
    picture pict;
    pict = "iXltfgqTApbj" infont f;
    1.2 * ypart(ulcorner(pict)-llcorner(pict))
endgroup
enddef;

def infontBB(expr s, f) =
begingroup
    save pict, pictb;
    picture pict, pictb;
    pict = s infont f;
    pictb = ("iXltfTAbgqjp" infont f scaled 1.2);
    setbounds pict to ulcorner(pictb) -- llcorner(pictb) -- 
	    lrcorner(pict) -- urcorner(pict) -- cycle;
    pict
endgroup
enddef;

%%%%%%%%%%%%%%%%%%%
%
%  Graphics for UML Elements


% A class title as a picture (font etc)
def diagramTitle(expr s) =
    (infontBB(s, "HelveticaBold") scaled 1.3)
enddef;

def classTitle(expr s) =
    (infontBB(s, defaultfont) scaled 1.5)
enddef;

def methodName(expr s) =
    (infontBB(s, defaultfont) scaled 0.8)
enddef;

def fieldName(expr s) =
    methodName(s)
enddef;

def adornmentName(expr s) =
    methodName(s)
enddef;

def naryassoc =
begingroup
    save pict;
    picture pict;
    pict := nullpicture;
    addto pict doublepath (0,20)--(30,0)--(0,-20)--(-30,0)--cycle withpen pencircle scaled 1pt;
    pict
endgroup
enddef;

def stereotype(expr s) =
% guillemets
    (infontBB( char(171) & s & char(187) , defaultfont) scaled 1.0)
enddef;

vardef agcopath(expr p) =
    % XXX Replace with impl that handles curves correctly
    save vx, vy, vc;
    pair vx, vy, vc;
    vc = point 0 of p;
    vx = direction 0 of p;
    vx := 5 * vx / (abs(vx) + 0.0001);
    vy = vx rotated 90;
    vx := 1.5*vx;
    vc -- vc+vx+vy -- vc+2*vx -- vc+vx-vy -- cycle
enddef;

vardef arrowedpath(expr p, lx, ly) =
    save vx, vy, vc;
    pair vx, vy, vc;
    vc = point 0 of p;
    vx = direction 0 of p;
    vx := 5 * vx / (abs(vx) + 0.0001);
    vy = ly * vx rotated 90;
    vx := lx*vx;
    vc+vx+vy -- vc -- vc+vx-vy 
enddef;

vardef inheritpath(expr p) =
    save vx, vy, vc;
    pair vx, vy, vc;
    vc = point length(p) of p;
    vx = -direction length(p) of p;
    vx := 10 * vx / (abs(vx) + 0.0001);
    vy = vx rotated 90;
    vc -- vc+vx+vy -- vc+vx -- vc+vx-vy -- cycle
enddef;

vardef locin(expr pict, x, y) =
    ( x[xpart(ulcorner(pict)), xpart(urcorner(pict))],
      y[ypart(llcorner(pict)), ypart(ulcorner(pict))]
    )
enddef;

vardef unitornullvector(expr p) =
    if length(p) > 0: unitvector(p)
    else: p
    fi
enddef;

vardef adornassocend(expr p, multi, role) =
    addto currentpicture also multi shifted 
	((point 0 of p) 
	+ (unitornullvector(direction 0 of p) zscaled (10,10))
	 -locin(multi,0.5,0.5));
    addto currentpicture also role shifted 
	((point 0 of p) 
	+ (unitornullvector(direction 0 of p) zscaled (10,-10))
	 -locin(role,0.5,0.5));
enddef;

% Aggregate in beginning of path
vardef aggregassoc(expr p, multi, role) =
    save ap;
    path ap;
    ap = agcopath(p);
    draw p;
    fill ap withcolor white;
    draw ap;
    adornassocend(p, multi, role);
enddef;

% Composite in beginning of path
vardef composassoc(expr p, multi, role) =
    save ap;
    path ap;
    ap = agcopath(p);
    draw p;
    fill ap withcolor black;
    draw ap;
    adornassocend(p, multi, role);
enddef;

vardef assoc(expr p, multi, role) =
    draw p;
    adornassocend(p, multi, role);
enddef;

vobtransformthick = .5 pt;
vobinthick = .7 pt;
vobsubmatchthick = 2pt;

vardef vobtransformfromassoc(expr p, multi, role) =
    save pe;
    pe = savepen;
    pickup pencircle scaled vobtransformthick;
    draw p;
    adornassocend(p, multi, role);
    pickup pe;
enddef;

vardef vobtransformtoassoc(expr p, multi, role) =
    save pe;
    pe = savepen;
    pickup pencircle scaled vobtransformthick;
    draw arrowedpath(p, 1, 1.3);
    draw p;
    adornassocend(p, multi, role);
    pickup pe;
enddef;

picture vobtranssubdash;
vobtranssubdash = dashpattern(on 8pt off 12pt);

vardef vobtransformfromsubassoc(expr p, multi, role) =
    save pe;
    pe = savepen;
    pickup pencircle scaled vobsubmatchthick;
    draw p dashed vobtranssubdash;
    pickup pencircle scaled vobtransformthick;
    draw p;
    adornassocend(p, multi, role);
    pickup pe;
enddef;

vardef vobtransformtosubassoc(expr p, multi, role) =
    save pe;
    pe = savepen;
    pickup pencircle scaled vobsubmatchthick;
    draw p dashed vobtranssubdash;
    draw arrowedpath(p, 1, 1.3);

    pickup pencircle scaled vobtransformthick;
    draw p;
    adornassocend(p, multi, role);
    pickup pe;
enddef;



vardef vobinfromassoc(expr p, multi, role) =
    save pe;
    pe = savepen;
    pickup pencircle scaled vobinthick;
    draw p dashed evenly;
    adornassocend(p, multi, role);
    pickup pe;
enddef;

vardef vobintoassoc(expr p, multi, role) =
    save pe;
    pe = savepen;
    pickup pencircle scaled vobinthick;
    draw arrowedpath(p, 1.4, 1.0);
    draw p dashed evenly;
    adornassocend(p, multi, role);
    pickup pe;
enddef;


vardef inherit(expr p) =
    save ap;
    path ap;
    ap = inheritpath(p);
    draw p;
    fill ap withcolor white;
    draw ap;
enddef;

vardef realize(expr p) =
    save ap;
    path ap;
    ap = inheritpath(p);
    draw p dashed evenly;
    fill ap withcolor white;
    draw ap;
enddef;

vardef vobsubmatch(expr p) =
    save pe;
    pe = savepen;
    pickup pencircle scaled vobsubmatchthick;
    draw p;
    draw arrowedpath(reversepath(p), 1.2, 1.4);
    pickup pe;
enddef;


vardef dep(expr p, ster) = 
    drawarrow p dashed evenly;
    picture q;
    q := nullpicture;
    addto q also stereotype(ster);
    addto currentpicture also q
%    shifted .5[lrcorner(p), ulcorner(p)];
    shifted (xpart llcorner(p) + ((xpart lrcorner(p) - xpart llcorner(p)) / 2 - ((xpart lrcorner(q) - xpart llcorner(q)) / 2)), ypart point .5 of p);
enddef;

%%%%%%%%%%%%%%%%%%%
% 
%  Stacking things

vardef stackStrings(expr font, scale)(text strs) =
    save p,b;
    picture p, b;
    p = nullpicture;
    for s = strs:
	b := infontBB(s, font) scaled scale;
	b := b shifted -llcorner b;
	p := p shifted ulcorner b;
	addto p also b;
    endfor;
    p
enddef;

vardef stackpics(text pics) =
    save p,b;
    picture p, b;
    p = nullpicture;
    for s = pics:
	b := s shifted -llcorner s;
	p := p shifted ulcorner b;
	addto p also b;
    endfor;
    p
enddef;

% If the width of b is larger than w, replace w with it. 
vardef maxwid(suffix w, b) =
    if not known w:
	w = 0;
    fi
    save wid;
    wid := xpart(urcorner b - ulcorner b);
    if wid > w:
	w := wid;
    fi
enddef;

% Center b in width w, make new bounding box.
vardef maxwidctr(suffix w, b) =
    save wid;
    save ctr;
    pair ctr;
    ctr = 0.5[urcorner b, llcorner b];
    wid := xpart(urcorner b - ulcorner b);
    if (wid < w) and (wid > 0):
      numeric margin;
      margin := bboxmargin;
      bboxmargin := 0;
      setbounds b to (bbox b shifted -ctr xscaled (w/wid) shifted ctr);
      bboxmargin := margin;
    fi
enddef;

%%%%%%%%%%%%%%%%%%%
%
%  Paths

% Reverse
vardef reversepath(expr p) =
    subpath (length p, 0) of p
enddef;

% Clip part of p inside the picmeasurements
vardef clipoutside(suffix a)(expr p) =
    ((p) cutbefore (a.n--a.ne--a.e--a.se--a.s--a.sw--a.w--a.nw--cycle))
enddef;


% picmeasurements in suffixes to draw default path between them: a line
% clipped by the boxes (or octagons, actually)
vardef backuppath(suffix a, b) =
    clipmeasuredpath(a, b, (a.c--b.c))
enddef;

vardef clipmeasuredpath(suffix a, b)(expr p) =
    reversepath(clipoutside(b, reversepath(clipoutside(a, p))))
enddef;


%%%%%%%%%%%%%%%%%%%
%
%  Hyperlinks to documentations

vardef strpair(expr p) =
    (decimal((xpart(p))) & "," & decimal((ypart(p))) )
enddef;
vardef showlink(expr target, title, p) =
    fill p withcolor (0.8, 0.9, 1);
    showlinksize(target, title, p);
enddef;
vardef showlinkerror(expr target, title, p) =
    showlinksize(target, title, p);
    draw classTitle("BROKEN LINK") shifted ulcorner(p) withcolor (1, 0, 0);
enddef;
vardef showfocus(expr target, title, p) =
    fill p withcolor (1, 0.8, 0.7);
    showlinksize(target, title, p);
enddef;
vardef showlinksize(expr target, title, p) =
    show "LINKRECT("& char(34) & target & char(34) & "," & char(34) & title & char(34) & "," & strpair((ulcorner(p))) &","& strpair((lrcorner(p))) &")"
enddef;

vardef jitterpt(expr p, s) =
    p + s * (normaldeviate, normaldeviate)
enddef;

vardef jitterpath(expr p, npt, pta) =
    save s;
    save i;
	for i = 0 step length(p)/npt until (length(p) * (npt-1.0)/npt):
	    jitterpt(point i of p, pta) ...
	endfor
    jitterpt(point length(p) of p, pta)
enddef;

vardef drawRoughEdge(expr p, q, scale) =
    save c, hor, ver, np, j, astart, athrough, aend, na;
    pair c;
    c = center(p);
    hor = 1.5 * xpart(llcorner p - c);
    ver = 1.5 * ypart(llcorner p - c);

    astart = uniformdeviate(360);
    athrough = 390 + 40 * normaldeviate;
    aend = astart + athrough;

    na = round(20 + 10 * normaldeviate);
    if na < 3 : na := 3; fi;

    path np;

    
    np = (sind(astart), cosd(astart)) 
	for i = 1 upto na:
	    .. (sind(astart + athrough/na*i),
	        cosd(astart + athrough/na*i))
	endfor;
    
    np := np xscaled(hor) yscaled(ver)  shifted(c);

    j = .15 * abs(hor);
    np := jitterpath(np, round(10+uniformdeviate(10)), .125 / scale * j);
    np := jitterpath(np, round(40+uniformdeviate(30)), .025 / scale * j);

    draw np withpen pencircle scaled (4pt/scale) xscaled .4 rotated -37;
    if known(q):
	clip currentpicture to q;;
    fi;
    
enddef;

%%%%%%%%%%%%%%%%%%%
%
%  Placement

vardef vertically(expr spacing)(suffix final)(text t) =
    save cur, had;
    had := 0;
    pair cur;
    pair final.s, final.n, final.c, final.w, final.e;
    forsuffixes obj = t:
	show "Vertically: ",cur, obj;
	if had = 0:
	    final.n = obj.n;
	    final.e = obj.e;
	    final.w = obj.w;
	    had := 1;
	fi
	obj.n = cur + (0, -spacing);
	if final.e < obj.e:
	    final.e := obj.e;
	fi
	if final.w > obj.w:
	    final.w := obj.w;
	fi
	save cur;
	pair cur;
	cur = obj.s ;
    endfor
    final.s = cur;
    final.c = 0.5[final.n, final.s];
    final.e := (xpart final.e, ypart final.c);
    final.w := (xpart final.w, ypart final.c);
enddef;


vardef horizontally(expr spacing)(suffix final)(text t) =
    save cur, had;
    had := 0;
    pair cur;
    pair final.w, final.e, final.c, final.s, final.n;
    forsuffixes obj = t:
	show "Vertically: ",cur, obj;
	if had = 0:
	    final.w = obj.w;
	    final.n = obj.n;
	    final.s = obj.s;
	    had := 1;
	fi
	obj.w = cur + (spacing, 0);
	if final.n < obj.n:
	    final.n := obj.n;
	fi
	if final.s > obj.s:
	    final.s := obj.s;
	fi
	save cur;
	pair cur;
	cur = obj.e ;
    endfor
    final.e = cur;
    final.c = 0.5[final.w, final.e];
    final.n := (xpart final.c, ypart final.n);
    final.s := (xpart final.c, ypart final.s);
enddef;

vardef centeroffs(expr spacing)(suffix final)(text t) =
    save cur, had;
    had := 0;
    pair cur;
    pair final.w, final.e, final.c;
    forsuffixes obj = t:
	had := had + 1;
	obj.c = cur + spacing;
	save cur;
	pair cur;
	cur = obj.c ;
    endfor
    final.c = cur - had/2 * spacing;
enddef;

%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Graphics for sequence diagrams

pen sequencecallpen, sequenceactivepen;

sequencecallpen = pencircle scaled 3pt;
sequenceactivepen = pencircle scaled 1.5pt;
pair sequencebwid, sequencex, sequencey;
sequencebwid = (5,0);
sequencex = (15,15);
sequencey = (-15,15);

vardef sequenceactivation(expr u,l) =
    save rectpath;
    path rectpath;
   rectpath = (u+sequencebwid) -- (l+sequencebwid) --
		(l-sequencebwid) -- (u-sequencebwid) -- cycle;
   fill rectpath withcolor white;
   draw rectpath withpen sequenceactivepen;
enddef;

vardef sequencedrawlifeline(suffix name)(expr y) =
    show "drawlifeline", name.c;
    if not known(ypart(name.c)):
	name.c = name.ghost.c;
	show "drawlifeline SET", name.c;
    fi
    draw name.s -- (xpart(name.s),y) withpen sequenceactivepen;
enddef;

vardef sequencecallmeasure(expr sourcex, destx, starty, endy, labelstring) =
   know(sourcex);
   know(destx);
   know(starty);
   know(endy);
enddef;

vardef sequencecall(expr sourcex, destx, starty, endy, labelstring) =
   save u, l, rectpath;
   pair u, l;
   u = (destx, starty);
   l = (destx, endy);
   sequenceactivation(u, l);
   drawarrow (sourcex, starty) -- u withpen sequencecallpen;
   drawarrow l -- (sourcex, endy) withpen sequencecallpen dashed evenly;
   label.top(labelstring, 0.5[(sourcex,starty), u]);
enddef;

vardef sequencedestroy(expr x, y) =
    save v, o;
    pair v, o;
    v = (x,y);
    draw v+sequencex -- v-sequencex withpen sequencecallpen;
    draw v+sequencey -- v-sequencey withpen sequencecallpen;
enddef;

vardef sequencecreatemeasure(expr sourcex)(suffix target)(expr starty, endy, labelstring) =
    know(sourcex);
    know(starty);
    know(endy);
    ypart(target.c) = starty;
enddef;
vardef sequencecreate(expr sourcex)(suffix target)(expr starty, endy, labelstring) =
    save dx;
    pair dx;
    if sourcex < xpart(target.c): dx = target.w; else: dx = target.e; fi
    save u,l;
    pair u,l;
    u = target.s;
    l = (xpart(target.c), endy);
    sequenceactivation(u, l);
    drawarrow (sourcex, starty) -- dx withpen sequencecallpen;
    drawarrow l -- (sourcex, endy) withpen sequencecallpen dashed evenly;
   label.top(labelstring, 0.5[(sourcex,starty), dx]);
enddef;
