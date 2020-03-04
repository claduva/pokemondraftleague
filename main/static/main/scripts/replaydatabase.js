$(document).ready(function() {
    table=$("#databasetable")
    for (x in replaydatabase){
        row=$("<tr></tr>")
        if (replaydatabase[x]['team1coach2__username']==""){
        row.append("<td>"+replaydatabase[x]['team1coach1__username']+"</td>")
        }
        else{
        row.append("<td>"+replaydatabase[x]['team1coach1__username']+" & "+replaydatabase[x]['team1coach2__username']+"</td>")
        }
        if (replaydatabase[x]['team2coach2__username']==""){
            row.append("<td>"+replaydatabase[x]['team2coach1__username']+"</td>")
        }
        else{
            row.append("<td>"+replaydatabase[x]['team2coach1__username']+" & "+replaydatabase[x]['team2coach2__username']+"</td>")
        }
        if (replaydatabase[x]['winnercoach2__username']==""){
            row.append("<td>"+replaydatabase[x]['winnercoach1__username']+"</td>")
            }
        else{
            row.append("<td>"+replaydatabase[x]['winnercoach1__username']+" & "+replaydatabase[x]['winnercoach2__username']+"</td>")
        }
        row.append("<td>"+replaydatabase[x]['replayuser1']+"</td>")
        row.append("<td>"+replaydatabase[x]['replayuser2']+"</td>")
        if (replaydatabase[x]['replay'].includes("Forfeit")||replaydatabase[x]['replay'].includes("Unavailable")){
            row.append("<td>"+replaydatabase[x]['replay']+"</td>")
        }
        else{
            row.append("<td><a href='"+replaydatabase[x]['replay']+"'>Replay</a></td>")
        }
        if (user){
        if (replaydatabase[x]['associatedmatch']!=""){
            row.append("<td><a href='/changeattribution/"+replaydatabase[x]['associatedmatch']+"'>Current ("+replaydatabase[x]['associatedmatch']+")</a></td>")
        }
        else{
            row.append("<td><a href='/changehistoricattribution/"+replaydatabase[x]['associatedhistoricmatch']+"'>Historic ("+replaydatabase[x]['associatedhistoricmatch']+")</a></td>")
        }
        }
        table.append(row)
       
    }

    $("#replaytable").tablesorter({
        widgets: ['filter'],
        ignoreCase: true,
    });

});
