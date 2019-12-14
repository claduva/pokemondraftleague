$(document).ready(function() {
  $("#sortby").change(function() {
        sortingby=$("#sortby").val()
        if (sortingby=="bst-dec"){
            sortMeBy("data-bst", $(".tieritem"), $("#tierlist"), "desc");
        }
        else if (sortingby=="bst-inc"){
            sortMeBy("data-bst", $(".tieritem"), $("#tierlist"), "asc");
        }
        else if (sortingby=="tier-dec"){
            sortMeBy("data-tier", $(".tieritem"), $("#tierlist"), "desc");
        }
        else if (sortingby=="tier-inc"){
            sortMeBy("data-tier", $(".tieritem"), $("#tierlist"), "asc");
        }
        else if (sortingby=="az"){
            sortMeByAlph("data-pokemon", $(".tieritem"), $("#tierlist"), "desc");
        }
        else if (sortingby=="za"){
            sortMeByAlph("data-pokemon", $(".tieritem"), $("#tierlist"), "asc");
        }
        else{
            console.log(sortingby)
        }
  });
  $("#available").change(function() {
    availablechoice=$("#available").val()
    tierchoice=$("#tierchoice").val()
    typingchoice=$("#typing").val()
    tl=$(".tieritem")
    if (availablechoice=="allpokemon"){
        tl.each(function(){
            item=$(this)
            item.removeClass('hidden-available')
            checkShow(item)
        })
    }
    else if (availablechoice=="available"){
        tl.each(function(){
            item=$(this)
            item.removeClass('hidden-available')
            checkShow(item)
            if (item.attr("data-available")!="FREE"){
                item.addClass('hidden-available')
                item.hide()
            }
        })
    }
  });
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

  $("#tiertable").hide()
  $("#tiertoggle").change(function() {
    if (this.checked) {
        $("#tiertable").show()
        $("#tierlist").hide()
        $(".filter").hide()
    } else {
        $("#tiertable").hide()
        $("#tierlist").show()
        $(".filter").show()
    }
})


});

function sortMeBy(arg, sel, elem, order) {
    sel.sort(function(a, b) {
        an = parseInt(a.getAttribute(arg)),
        bn = parseInt(b.getAttribute(arg));
        astring = a.getAttribute("data-pokemon"),
        bstring = b.getAttribute("data-pokemon");
        if (order == "asc") {
        if (an > bn) return 1;
        if (an < bn) return -1;
        else return astring.localeCompare(bstring)
        } else if (order == "desc") {
        if (an < bn) return 1;
        if (an > bn) return -1;
        else return astring.localeCompare(bstring)
        }
        return 0;
    });
    sel.detach().appendTo(elem)
}

function sortMeByAlph(arg, sel, elem, order) {
    sel.sort(function(a, b) {
        an = a.getAttribute(arg),
        bn = b.getAttribute(arg);
        if (order == "asc") {
            return bn.localeCompare(an); 
        } else if (order == "desc") {
            return an.localeCompare(bn); 
        }
        return 0;
    });
    sel.detach().appendTo(elem)
}

function checkShow(item){
    if(item.hasClass('hidden-type')==false && item.hasClass('hidden-tier')==false && item.hasClass('hidden-available')==false){
        item.show()
    }
}