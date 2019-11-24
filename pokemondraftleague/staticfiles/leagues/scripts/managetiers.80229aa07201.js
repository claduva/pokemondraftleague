$(document).ready(function() {
    $("#leftarrow").click(function() {
        alert('left')
    });
  });
  
  function sortMeByAlph(arg, sel, elem, order) {
      sel.sort(function(a, b) {
          an = a.getAttribute(arg),
          bn = b.getAttribute(arg);
          if (order == "asc") {
              return bn.localeCompare(an); 
          } else if (order == "desc") {
              return an.localeCompare(bn); 
          }
          return 0;
      });
      sel.detach().appendTo(elem)
  }