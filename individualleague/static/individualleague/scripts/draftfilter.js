$(document).ready(function() {
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