$(document).ready(function() {
    
    //current
    currentmatches=$(".currentmatchid")
    currentmatches.each(function() {
        currentmatch=$(this)
        $.post(
            "/checkanalyzer/currentmatch/",
            {
              matchid: currentmatch.text(),
            },
            function(data) {
                $("#currentreplaybox").empty()
                $("#currentreplaybox").append("<span>"+data.replay+"</span>")
                newnum=parseInt($("#currentprogress").text())+1
                $("#currentprogress").text(newnum)
                if (!data.success){
                  $("#failedreplays").append("<div>"+data.replay+"</div>")
                  newnum=parseInt($("#failcount").text())+1
                  $("#failcount").text(newnum)
                }
            }
          );
    })

    //historic
    historicalmatches=$(".historicalmatchid")
    historicalmatches.each(function() {
        currentmatch=$(this)
        $.post(
            "/checkanalyzer/histmatch/",
            {
              matchid: currentmatch.text(),
            },
            function(data) {
                $("#histreplaybox").empty()
                $("#histreplaybox").append("<span>"+data.replay+"</span>")
                newnum=parseInt($("#histprogress").text())+1
                $("#histprogress").text(newnum)
                if (!data.success){
                  $("#failedreplays").append("<div>"+data.replay+"</div>")
                  newnum=parseInt($("#failcount").text())+1
                  $("#failcount").text(newnum)
                }
            }
          );
    })

});

