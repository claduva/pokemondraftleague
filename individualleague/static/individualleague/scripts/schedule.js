$(document).ready(function() {
    $("#weekselect").change(function() {
        weekselect=$("#weekselect").val()
        if (weekselect=="All"){
            $(".scheduleweek").show()
        }
        else{
            $(".scheduleweek").hide()
            $("#week-"+weekselect).show()
        }
    })
});
