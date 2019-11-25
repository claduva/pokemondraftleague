$(document).ready(function() {
    $("td").on("click",".leftarrow",function() {
        pi=$(this).parent("div")
        parentcolumn=pi.parent("td")
        // check if has r arrow
        pi.not(":has(span.rightarrow)").append("<span class='rightarrow'>&rarr;</span>")
        newparentcolumn=parentcolumn.prev("td")
        if (newparentcolumn.prev("td.wt").length==0) {
            pi.find(".leftarrow").detach()
        }
        pi.detach()
        newparentcolumn.append(pi)
        newparentcolumn.children("div").sort(asc_sort).appendTo(newparentcolumn);
        tierid=pi.data("tierid")
        pokemonid=pi.data("pokemonid")
        parentth = newparentcolumn.closest('table').find('th').eq(newparentcolumn.index());
        newtierid=parentth.data("tier")
        $.post(
            "/settings/updatetiering/",
            {
                tierid: tierid,
                newtierid: newtierid,
                pokemonid: pokemonid,
            },
            function(data) {
            }
          );
    });

    /* $(".leftarrow").on("click",function() {
        pi=$(this).parent("div")
        parentcolumn=pi.parent("td")
        // check if has r arrow
        pi.not(":has(span.rightarrow)").append("<span class='rightarrow'>&rarr;</span>")
        newparentcolumn=parentcolumn.prev("td")
        if (newparentcolumn.prev("td.wt").length==0) {
            pi.find(".leftarrow").detach()
        }
        pi.detach()
        newparentcolumn.append(pi)
        newparentcolumn.children("div").sort(asc_sort).appendTo(newparentcolumn);
        tierid=pi.data("tierid")
        pokemonid=pi.data("pokemonid")
        parentth = newparentcolumn.closest('table').find('th').eq(newparentcolumn.index());
        newtierid=parentth.data("tier")
        $.post(
            "/settings/updatetiering/",
            {
                tierid: tierid,
                newtierid: newtierid,
                pokemonid: pokemonid,
            },
            function(data) {
            }
          );
    }); */

    $("td").on("click",".rightarrow",function() {
        pi=$(this).parent("div")
        parentcolumn=pi.parent("td")
        // check if has l arrow
        pi.not(":has(span.leftarrow)").prepend("<span class='leftarrow'>&larr;</span>")
        newparentcolumn=parentcolumn.next("td")
        if (newparentcolumn.next("td").length==0) {
            pi.find(".rightarrow").detach()
        }
        if (newparentcolumn.prev("td.wt").length==0) {
            pi.find(".leftarrow").detach()
        }
        pi.detach()
        newparentcolumn.append(pi)
        newparentcolumn.children("div").sort(asc_sort).appendTo(newparentcolumn);
        tierid=pi.data("tierid")
        pokemonid=pi.data("pokemonid")
        parentth = newparentcolumn.closest('table').find('th').eq(newparentcolumn.index());
        newtierid=parentth.data("tier")
        $.post(
            "/settings/updatetiering/",
            {
                tierid: tierid,
                newtierid: newtierid,
                pokemonid: pokemonid,
            },
            function(data) {
            }
          );
    });
});

function asc_sort(a, b){
    return ($(b).text()) < ($(a).text()) ? 1 : -1;    
}

function dec_sort(a, b){
    return ($(b).text()) > ($(a).text()) ? 1 : -1;    
} 