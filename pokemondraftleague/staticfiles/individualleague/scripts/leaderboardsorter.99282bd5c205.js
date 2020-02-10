$(document).ready(function() {
  //initialize header
  sortheaders = $("th.sort")
  alert("here")
  sortheaders.append("<span>&uarr;&darr;<span>").addClass("unsorted");
/* 
  //unsorted
  $("tr").on("click", "th.unsorted", function() {
    sortheaders.children("span").html("&uarr;&darr;");
    sortheaders
      .addClass("unsorted")
      .removeClass("asc")
      .removeClass("desc");
    //change span
    $(this)
      .children("span")
      .html("&darr;");
    $(this)
      .addClass("desc")
      .removeClass("unsorted")
      .removeClass("asc");

    index = $(this).index();
    table = $(this).closest("table");
    sortTable(index, "desc", table);
  });

  //asc
  $("tr").on("click", "th.asc", function() {
    sortheaders.children("span").html("&uarr;&darr;");
    sortheaders
      .addClass("unsorted")
      .removeClass("asc")
      .removeClass("desc");
    table = $(this).closest("table");
    sortTable(0, "asc", table);
  });

  //desc
  $("tr").on("click", "th.desc", function() {
    sortheaders.children("span").html("&uarr;&darr;");
    sortheaders
      .addClass("unsorted")
      .removeClass("asc")
      .removeClass("desc");
    //change span
    $(this)
      .children("span")
      .html("&uarr;");
    $(this)
      .removeClass("desc")
      .removeClass("unsorted")
      .addClass("asc");

    index = $(this).index();
    table = $(this).closest("table");
    sortTable(index, "asc", table);
     */
  });
});

function sortTable(n, dir, table) {
  var rows,
    switching,
    i,
    x,
    y,
    shouldSwitch,
    switchcount = 0;
  switching = true;
  /* Make a loop that will continue until
    no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.find("tr");
    headingsize=table.find("tr.th").length
    /* Loop through all table rows (except the
      first, which contains table headers): */
    for (i = headingsize; i < rows.length - 1; i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
        one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      console.log($.isNumeric(x.innerHTML));
      /* Check if the two rows should switch place,
        based on the direction, asc or desc: */
      if (dir == "desc" && $.isNumeric(x.innerHTML)) {
        if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML)) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "asc" && $.isNumeric(x.innerHTML)) {
        if (parseFloat(x.innerHTML) > parseFloat(y.innerHTML)) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
        } else if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount++;
    } else {
      /* If no switching has been done AND the direction is "asc",
        set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
