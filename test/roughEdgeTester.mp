prologues := 2;
input ../navidoc/mp/uml;

beginfig(1);

path cli;


mx = 0;
for w = 5 step 4 until 100:
 my := 0;
 for h = 5 step 4 until 100:
    show mx, my;
    path pa;
    pa := unitsquare xscaled w yscaled h shifted (mx, my);
    draw pa;
    pair pai;

    drawRoughEdge(pa, cli, .3);
    my := my + h + 30;
 endfor;
 mx := mx + w + 30;
endfor;

endfig;
end
