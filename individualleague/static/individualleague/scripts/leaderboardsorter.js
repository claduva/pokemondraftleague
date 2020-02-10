$(document).ready(function() {
  $("#leadertable").tablesorter();

  var table = $("#leadertable");
  table.bind("sortEnd", function() {
    var i
    $("td.rownum").each(function(i) {
      $(this).text(i+1)
    })
  });
});
