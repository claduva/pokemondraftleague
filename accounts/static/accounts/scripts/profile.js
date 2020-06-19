$(document).ready(function() {
    acquiredtable=$("#mostacquired").find("table")
    for (x in mostacquired){
        li=mostacquired[x]
        tr=$("<tr></tr")
        td1=$("<td><img class='smallsprite' src='"+li[2]+"'>"+li[0]+"</td>")
        td2=$("<td>"+li[1]+"</td>")
        tr.append(td1,td2)
        acquiredtable.append(tr)
    }

    rivaltable=$("#rivals").find("table")
    for (x in rivallist){
        li=rivallist[x]
        tr=$("<tr></tr")
        td1=$("<td>"+li[0]+"</td>")
        td2=$("<td>"+li[1]+"</td>")
        td3=$("<td>"+li[2]+"</td>")
        tr.append(td1,td2,td3)
        rivaltable.append(tr)
    }

    favoritemovetable=$("#favmoves").find("table")
    for (x in favoritemovelist){
        li=favoritemovelist[x]
        tr=$("<tr></tr")
        td1=$("<td>"+li[0]+"</td>")
        td2=$("<td>"+li[1]+"</td>")
        td3=$("<td>"+li[2]+"</td>")
        td4=$("<td>"+li[3]+"</td>")
        td5=$("<td>"+li[5]+"/"+li[4]+"</td>")
        tr.append(td1,td2,td3,td4,td5)
        favoritemovetable.append(tr)
    }

    allmatchestable=$("#allmatches").find("table")
    for (x in matchlist){
        li=matchlist[x]
        tr=$("<tr class='matchitem'></tr")
        if (li[2].includes("Playoff")){
            tr.addClass("Playoffs")
        }
        if (li[5]>0){
            tr.addClass("Win")
        }
        else{
            tr.addClass("Loss")
        }
        if (li[4].includes("Forfeit")){
            tr.addClass("Forfeit")
            td5=$("<td>Forfeit</td>")
        }
        else{
            td5=$("<td><a href='"+li[4]+"'>Link</a</td>")
        }
        td1=$("<td>"+li[0]+"</td>")
        td2=$("<td>"+li[1]+"</td>")
        td3=$("<td>"+li[2]+"</td>")
        td4=$("<td>"+li[3]+"</td>")
        if (li[7]=="False"){
            td6=$("<td class='nonfavorite'><div class='replayid' hidden>"+li[6]+"</div><img class='x-smallsprite' src='/static/main/images/emptystar.png' ></td>")
        }
        else{
            td6=$("<td class='favorite'><div class='replayid' hidden>"+li[6]+"</div><img class='x-smallsprite' src='/static/main/images/goldstar.png' ></td>")
            tr.addClass("Favorite")
        }
        if (isuser){tr.append(td6,td1,td2,td3,td4,td5)}
        else{tr.append(td1,td2,td3,td4,td5)}
        allmatchestable.append(tr)
    }

    $("#tableselector").change(function(){
        sel=$("#tableselector").val()
        $(".profiletable").addClass("d-none")
        $("#"+sel).removeClass("d-none")
    })

    $("#matchfilter").change(function(){
        sel=$("#matchfilter").val()
        if (sel=="All"){
            $(".matchitem").removeClass("d-none")
        }
        else if (sel=="Wins"){
            $(".matchitem").addClass("d-none")
            $(".Win").removeClass("d-none")
        }
        else if (sel=="Losses"){
            $(".matchitem").addClass("d-none")
            $(".Loss").removeClass("d-none")
        }
        else if (sel=="ffwins"){
            $(".matchitem").addClass("d-none")
            $(".Win.Forfeit").removeClass("d-none")
        }
        else if (sel=="fflosses"){
            $(".matchitem").addClass("d-none")
            $(".Loss.Forfeit").removeClass("d-none")
        }
        else if (sel=="Playoffs"){
            $(".matchitem").addClass("d-none")
            $(".Playoffs").removeClass("d-none")
        }
        else if (sel=="Favorites"){
            $(".matchitem").addClass("d-none")
            $(".Favorite").removeClass("d-none")
        }
    })

    $("tr").on('click','.nonfavorite',function(){
        $(this).addClass("favorite").removeClass("nonfavorite")
        $(this).find('img').remove()
        $(this).append("<img class='x-smallsprite' src='/static/main/images/goldstar.png' >")
        $(this).closest("tr").addClass('Favorite')
        $.post(
            "/addfavorite/",
            {
              matchid: $(this).find(".replayid").text(),
            },
            function(data) {
             
            }
        );
    })

    $("tr").on('click','.favorite',function(){
        $(this).removeClass("favorite").addClass("nonfavorite")
        $(this).find('img').remove()
        $(this).append("<img class='x-smallsprite' src='/static/main/images/emptystar.png' >")
        $(this).closest("tr").removeClass('Favorite')
        $.post(
            "/removefavorite/",
            {
              matchid: $(this).find(".replayid").text(),
            },
            function(data) {
             
            }
        );
    })
})
