$(document).ready(function() {
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