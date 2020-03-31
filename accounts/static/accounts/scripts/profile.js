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
        td6=$("<td class='favorite'><img class='x-smallsprite' src='/static/main/images/emptystar.png' ></td>")
        tr.append(td6,td1,td2,td3,td4,td5)
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
        }
    })

    $("tr").on('click','.nonfavorite',function(){
        console.log('select')
        $(this).empty().addClass("favorite").removeClass("nonfavorite")
        $(this).append("<img class='x-smallsprite' src='/static/main/images/goldstar.png' >")
    })

    $("tr").on('click','.favorite',function(){
        console.log('unselect')
        $(this).empty().removeClass("favorite").addClass("nonfavorite")
        $(this).append("<img class='x-smallsprite' src='/static/main/images/emptystar.png' >")
    })
})
