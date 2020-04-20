$(document).ready(function() {
   
    $("#id_league_").change(function(){
    associatedleague=$("#id_league_").val()
    $.post(
        "/uploadhistoricrender/",
        {
          associatedleague: associatedleague,
          purpose:"Add Seasons"
        },
        function(data) {
            seasons=data.seasons
            seasonfield=$("#id_seasonname")
            for(x in seasons){
                seasonfield.append("<option value='"+seasons[x]+"'>"+seasons[x]+"</option>")
            }
        }
      );
   })
    
   $("#id_seasonname").change(function(){
    associatedleague=$("#id_league_").val()
    seasonname=$("#id_seasonname").val()
    $.post(
        "/uploadhistoricrender/",
        {
          associatedleague: associatedleague,
          seasonname:seasonname,
          purpose:"Add Teams"
        },
        function(data) {
            teams=data.teams
            team1field=$("#id_team1")
            team2field=$("#id_team2")
            winnerfield=$("#id_winner")
            for(x in teams){
                team1field.append("<option value='"+teams[x]+"'>"+teams[x]+"</option>")
                team2field.append("<option value='"+teams[x]+"'>"+teams[x]+"</option>")
                winnerfield.append("<option value='"+teams[x]+"'>"+teams[x]+"</option>")
            }
        }
      );
   })
});
