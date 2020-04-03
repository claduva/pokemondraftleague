$(document).ready(function() {
    
  for (x in team1effectiveness){
    img=$("<img class='smallsprite' src='"+team1effectiveness[x][0]+"'>")
    for ( [key, value] of Object.entries(team1effectiveness[x][1])){
      cl=key.charAt(0).toUpperCase() + key.slice(1)+value
      $(".team1 ."+cl).append(img.clone())
    }
  }

  for (x in team2effectiveness){
    img=$("<img class='smallsprite' src='"+team2effectiveness[x][0]+"'>")
    for ( [key, value] of Object.entries(team2effectiveness[x][1])){
      cl=key.charAt(0).toUpperCase() + key.slice(1)+value
      $(".team2 ."+cl).append(img.clone())
    }
  }
  
  $("div").on("click", "button.matchup-menu", function() {
      $("div button.matchup-menu").removeClass('btn-dark').addClass('btn-primary')
      $(this).removeClass('btn-primary').addClass('btn-dark')
      $(".section").hide()
      idoi=$(this).text().toLowerCase().replace(/ /g,"")
      $("#"+idoi).show()
    });
  
  
  lvl50=$(".lvl50")
  lvl50.hide()
  lvl100=$(".lvl100")
  $("#lvltoggle").change(function() {
      if (this.checked) {
        lvl100.show()
      lvl50.hide()
      } else {
        lvl100.hide()
        lvl50.show()
      }
  })
});
