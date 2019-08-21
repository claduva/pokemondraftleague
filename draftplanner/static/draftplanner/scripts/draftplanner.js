$(document).ready(function() {
    //add mon
    $("#addmon").click(function(){
        $("#topmonlist").prepend("<div class='col-1 bg-lightgrey text-dark text-center border'><img src='https://play.pokemonshowdown.com/sprites/xyani/unown-question.gif'></div>")
    });

    //searchbox  
    $("#moninput").keyup(function() {
        lookupmon=$("#moninput").val()
        $.post(
        "/draftplanner/getmon",
        {
            'lookupmon': lookupmon,
        },
        function(data){
            $("#monsearchlist").empty()
            for (i = 0; i < data.length; i++) { 
                $("#monsearchlist").append("<div class='col-12 border monsearchlistitem'>"+data[i].fields.pokemon+"</div>")
            }
        });
    });

    
});
