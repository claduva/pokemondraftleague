$(document).ready(function() {
    // insert table
    tableheads=$("#tableheads")
    tablebody=$("#tablebody")
    for (x in tierdict){
        tableheads.append('<th class="bg-dark text-light">'+tierdict[x][0][1]+' ('+tierdict[x][0][2]+' pts)'+'</th>')
        ita1=$('<td class="p-0 m-0"></td>')
        for (y in tierdict[x]){
            itemdata=JSON.parse(tierdict[x][y][3])
            spriteurl=itemdata[tierdict[x][y][0]]['sprites'][sprite]
            if (tierdict[x][y][5]=="FREE"){
                ita2=$('<div style="height:30px;" class="bg-green border border-dark"></div>')
            }
            else{
                ita2=$('<div style="height:30px;" class="bg-red border border-dark"></div>')
            }
            ita2.append(tierdict[x][y][5]+'<img class="smallsprite" src="'+spriteurl+'">'+tierdict[x][y][0])
            ita1.append(ita2)
        }
        tablebody.append(ita1)
    }

    // insert tierlist
    tl=$("#tierlist")
    for (x in tierlist) {
        pokemon=tierlist[x][0]
        tiername=tierlist[x][1]
        tierpoints=tierlist[x][2]
        itemdata=JSON.parse(tierlist[x][3])
        availability=tierlist[x][5]
        eta1=$("<div class='tieritem'></div>")
        eta1.attr('data-tier',tierpoints)
        eta1.attr('data-bst',itemdata[pokemon]['basestats']['bst'])
        eta1.attr('data-hp',itemdata[pokemon]['basestats']['hp'])
        eta1.attr('data-atk',itemdata[pokemon]['basestats']['attack'])
        eta1.attr('data-def',itemdata[pokemon]['basestats']['defense'])
        eta1.attr('data-spa',itemdata[pokemon]['basestats']['s_attack'])
        eta1.attr('data-spd',itemdata[pokemon]['basestats']['s_defense'])
        eta1.attr('data-speed',itemdata[pokemon]['basestats']['speed'])
        eta1.attr('data-pokemon',pokemon)
        eta1.attr('data-available',availability)
        eta2=$("<a href=''></a>")
        spriteurl=itemdata[pokemon]['sprites'][sprite]
        if (availability=="FREE"){
            eta3=$("<div class='row bg-green text-dark rounded mb-1'></div>")
            eta4=$("<div class='col-3 col-md-2 justify-content-center d-flex align-items-center'><div class='text-center'>"+availability+"</div></div>")
        }
        else{
            eta3=$("<div class='row bg-red text-dark rounded mb-1'></div>")
            eta4=$("<div class='col-3 col-md-2 justify-content-center d-flex align-items-center'><div class='text-center'>Signed by "+availability+"</div></div>")
        }
        eta5=$('<div class="col-3 col-md-2 text-center align-middle"><div>'+tiername+'</div><div>('+tierpoints+' pts)</div></div>')
        eta6=$('<div class="col-3 col-md-2 d-flex justify-content-center align-items-center"><img class="smallsprite" src="'+spriteurl+'">'+pokemon+'</div>')
        eta7=$('<div class="col-3 col-md-2 d-flex justify-content-center align-items-center"><div></div></div>')
        types=itemdata[pokemon]['types']
        for (y in types) {
            typing=types[y]
            eta8=$('<div><img src="/static/pokemondatabase/sprites/types/'+typing+'.png"></div><div class="'+typing+'" hidden>'+typing+'</div>')
            eta7.append(eta8)
        }
        eta9=$('<div class="col-12 col-md-4 d-flex justify-content-center"></div>')
        eta9.append('<div class="px-1"><div><small>HP</small></div><div><small>'+itemdata[pokemon]['basestats']['hp']+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>Atk</small></div><div><small>'+itemdata[pokemon]['basestats']['attack']+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>Def</small></div><div><small>'+itemdata[pokemon]['basestats']['defense']+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>SpA</small></div><div><small>'+itemdata[pokemon]['basestats']['s_attack']+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>SpD</small></div><div><small>'+itemdata[pokemon]['basestats']['s_defense']+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>Spe</small></div><div><small>'+itemdata[pokemon]['basestats']['speed']+'</small></div></div>')
        eta9.append('<div class="px-1"><div><small>BST</small></div><div><small>'+itemdata[pokemon]['basestats']['bst']+'</small></div></div>')
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
