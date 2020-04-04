$(document).ready(function() {
    availabletable=$("#availabletable")
    for (x in availablejson){
        name=availablejson[x][0]
        tier=availablejson[x][1]
        points=availablejson[x][2]
        url=availablejson[x][3]
        a=$('<tr class="tieritem"></tr>')
        a.attr('data-tier',points)
        datatable=JSON.parse(availablejson[x][3])
        types=datatable[name]['types']
        url=datatable[name]['sprites'][spritesettings[0]]
        console.log(url)
        b=$('<td></td>')
        c=$('<img class="smallsprite" src="'+url+'"><span>'+name+' ('+tier+': '+points+' pts)</span>')
        b.append(c)
        for (y in types){
            typing=types[y]
            b.append('<div class="'+typing+'" hidden>'+typing+'</div>')
        }
        a.append(b)
        availabletable.append(a)
    }

    $("#tierchoice").change(function() {
    availablechoice=$("#available").val()
    tierchoice=$("#tierchoice").val()
    typingchoice=$("#typing").val()
    tl=$(".tieritem")
    if (tierchoice=="none"){
        tl.each(function(){
            item=$(this)
            item.removeClass('hidden-tier')
            checkShow(item)
        })
    }
    else {
        tl.each(function(){
            item=$(this)
            item.removeClass('hidden-tier')
            checkShow(item)
            if (item.attr("data-tier")!=tierchoice){
                item.addClass('hidden-tier')
                item.hide()
            }
        })
    }
  });
  $("#typing").change(function() {
    availablechoice=$("#available").val()
    tierchoice=$("#tierchoice").val()
    typingchoice=$("#typing").val()
    tl=$(".tieritem")
    if (typingchoice=="none"){
        tl.each(function(){
            item=$(this)
            item.removeClass('hidden-type')
            checkShow(item)
        })
    }
    else {
        tl.each(function(){
            item=$(this)
            item.removeClass('hidden-type')
            checkShow(item)
            if (item.find("."+typingchoice).length==0){
                item.hide()
                item.addClass('hidden-type')
            }
        })
    }
  });
})

function checkShow(item){
    if(item.hasClass('hidden-type')==false && item.hasClass('hidden-tier')==false){
        item.show()
    }
}