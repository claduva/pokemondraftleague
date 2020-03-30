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
})
