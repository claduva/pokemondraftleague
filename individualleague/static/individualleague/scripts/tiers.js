$(document).ready(function() {
    tl=$("#tierlist")
    for (x in tierlist) {
        eta1=$("<div class='tieritem'></div>")
        eta1.attr('data-tier',tierlist[x][3])
        eta1.attr('data-bst',tierlist[x][12])
        eta1.attr('data-hp',tierlist[x][6])
        eta1.attr('data-atk',tierlist[x][7])
        eta1.attr('data-def',tierlist[x][8])
        eta1.attr('data-spa',tierlist[x][9])
        eta1.attr('data-spd',tierlist[x][10])
        eta1.attr('data-speed',tierlist[x][11])
        eta1.attr('data-pokemon',tierlist[x][0])
        eta1.attr('data-available',tierlist[x][1])
        eta2=$("<a href=''></a>")
        if (tierlist[x][1]=="FREE"){
            eta3=$("<div class='row bg-green text-dark rounded mb-1'></div>")
        }
        else{
            eta3=$("<div class='row bg-red text-dark rounded mb-1'></div>")
        }
        eta4=$("<div class='col-3 col-md-2 justify-content-center d-flex align-items-center'><div class='text-center'>"+tierlist[x][1]+"</div></div>")
        eta5=$('<div class="col-3 col-md-2 text-center align-middle"><div>'+tierlist[x][2]+'</div><div>('+tierlist[x][3]+' pts)</div></div>')
        eta6=$('<div class="col-3 col-md-2 d-flex justify-content-center align-items-center"><img class="smallsprite" src="'+tierlist[x][4]+'">'+tierlist[x][0]+'</div>')
        eta7=$('<div class="col-3 col-md-2 d-flex justify-content-center align-items-center"><div></div></div>')
        for (y in tierlist[x][5]) {
            eta8=$('<div><img src="/static/pokemondatabase/sprites/types/'+tierlist[x][5][y]+'.png"></div><div class="'+tierlist[x][5][y]+'" hidden>'+tierlist[x][5][y]+'</div>')
            eta7.append(eta8)
        }
        eta9=$('<div class="col-12 col-md-4 d-flex justify-content-center"></div>')
        eta9.append('<div class="px-1"><div><small>HP</small></div><div><small>'+tierlist[x][6]+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>Atk</small></div><div><small>'+tierlist[x][7]+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>Def</small></div><div><small>'+tierlist[x][8]+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>SpA</small></div><div><small>'+tierlist[x][9]+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>SpD</small></div><div><small>'+tierlist[x][10]+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>Spe</small></div><div><small>'+tierlist[x][11]+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>BST</small></div><div><small>'+tierlist[x][12]+'</small></div></div>')
        eta3.append(eta4)
        eta3.append(eta5)
        eta3.append(eta6)
        eta3.append(eta7)
        eta3.append(eta9)
        eta2.append(eta3)
        eta1.append(eta2)
        tl.append(eta1)
    }
});
