$(document).ready(function() {
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
