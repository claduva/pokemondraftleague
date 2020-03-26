$(document).ready(function() {
  //configure searchlist
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading d-none'><div class='col-12'>Pokemon</div></div>")
  for (x in pokemondatabase){
    jsonitem=JSON.parse(pokemondatabase[x])
    itemname=Object.keys(jsonitem)[0]
    outer=$("<div class='row p-1 border border-dark bg-lightgrey text-dark monsearchlistitem d-none'></div>")
    outer.append("<div class='col-2 d-flex justify-content-center align-items-center'><img class='smallsprite searchlistimg' src='"+jsonitem[itemname]['sprites'][spriteurl]+"'><span class='searchlistname'>"+itemname+"</span></div>")
    inner=$("<div class='col-1 d-flex justify-content-center align-items-center'></div>")
    for (type in jsonitem[itemname]['types']){
      inner.append("<div><img class='searchlisttype' src='/static/pokemondatabase/sprites/types/"+jsonitem[itemname]['types'][type]+".png'></div>")
    }
    outer.append(inner)
    inner=$("<div class='col-3 text-center my-auto'></div>")
    inner.append("<small class='searchlistability'>"+jsonitem[itemname]['abilities'].join(", ")+"</small>")
    outer.append(inner)
    inner=$("<div class='col-3 my-auto'></div>")
    inner.append('<div class="text-dark text-center"><table class="table table-sm p-0 m-0 text-center"><tr class="statstable"><td>'+jsonitem[itemname]['basestats']['hp']+'</td><td>'+jsonitem[itemname]['basestats']['attack']+'</td><td>'+jsonitem[itemname]['basestats']['defense']+'</td><td>'+jsonitem[itemname]['basestats']['s_attack']+'</td><td>'+jsonitem[itemname]['basestats']['s_defense']+'</td><td>'+jsonitem[itemname]['basestats']['speed']+'</td><td>'+jsonitem[itemname]['basestats']['bst']+'</td></tr></table></div>')
    outer.append(inner)
    inner=$("<div class='col-3 my-auto text-center'></div>")
    learnset=jsonitem[itemname]['learnset']
    learnset=Object.keys(learnset)
    useful=[]
    for (move in learnset){
      if(learnset[move]=='Stealth Rock'||learnset[move]=='Spikes'||learnset[move]=='Toxic Spikes'||learnset[move]=='Sticky Web'||learnset[move]=='Defog'||learnset[move]=='Rapid Spin'||learnset[move]=='Court Change'||learnset[move]=='Heal Bell'||learnset[move]=='Aromatherapy'||learnset[move]=='Wish'){
        useful.push(learnset[move])
      }
    }
    if (useful.join(", ")==""){
      inner.append("<small class='searchlistmoves'>-</small>")
    }
    else{
      inner.append("<small class='searchlistmoves'>"+useful.join(", ")+"</small>")
    }
    outer.append(inner)
    $("#monsearchlist").append(outer)
  }
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading d-none'><div class='col-12'>Types</div></div>")
  for (x in typelist){
    $("#monsearchlist").append("<div class='row p-1 border border-dark bg-lightgrey text-dark d-none'><div class='col-12'>"+typelist[x]+"</div></div>")
  }
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading d-none'><div class='col-12'>Abilities</div></div>")
  for (x in abilitylist){
    $("#monsearchlist").append("<div class='row p-1 border border-dark bg-lightgrey text-dark d-none'><div class='col-12'>"+abilitylist[x]+"</div></div>")
  }
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading d-none'><div class='col-12'>Moves</div></div>")
  for (x in movelist){
    $("#monsearchlist").append("<div class='row p-1 border border-dark bg-lightgrey text-dark d-none'><div class='col-12'>"+movelist[x]+"</div></div>")
  }

  //clicking searchlist
  $(".monsearchlistitem").click(function() {
    selectedimgsm=$(this).find(".searchlistimg").clone()
    selectedimgmd=$(this).find(".searchlistimg").clone().removeClass('smallsprite').addClass('mediumsprite')
    selectedname=$(this).find(".searchlistname").text()
    selectedtyping=$(this).find(".searchlisttype").clone()
    selectedability=$(this).find(".searchlistability").clone()
    selectedstats=$(this).find(".statstable").html()
    selectedmoves=$(this).find(".searchlistmoves").clone()
    $("#selectedmon").html(selectedimgmd)
    $("#moninput").val(selectedname)
    $("#typingbox").html(selectedtyping)
    $("#abilitybox").html(selectedability)
    $("#statbox").html(selectedstats)
    $("#movesbox").html(selectedmoves)
    $(".activemon").html(selectedimgmd.clone()).removeClass('nomonselected')
    $(".activemon").append('<div class="topname" hidden></div><div class="toptypes" hidden></div><div class="topabilities" hidden></div><div class="topstats" hidden></div><div class="topmoves" hidden></div>')
    $(".activemon .topname").append(selectedname)
    $(".activemon .toptypes").append(selectedtyping.clone())
    $(".activemon .topabilities").append(selectedability.clone())
    $(".activemon .topstats").append(selectedstats)
    $(".activemon .topmoves").append(selectedmoves.clone())
    $(".searchheading").addClass('d-none')
    $(".monsearchlistitem").addClass('d-none')
    savedraft()
    updatedata()
  })

  //searchbox
  $("#moninput").keyup(function() {
    lookup = $("#moninput").val();
    if (lookup != ""){
    $(".searchheading").removeClass('d-none')
    $(".monsearchlistitem").each(function() {
      lu=String(lookup).toLowerCase()
      if ($(this).find(".searchlistname").text().toLowerCase().includes(lu)){
        $(this).removeClass('d-none')
      }
      else{
        $(this).addClass('d-none')
      }
    })
    }
    else{
      $(".searchheading").addClass('d-none')
      $(".monsearchlistitem").addClass('d-none')
    }
  })

  //addmon
  $("#addmon").click(addMon)

  //click top mon
  $("div").on("click",".topmon",function() {
    $(".activemon").removeClass("activemon").addClass("bg-lightgrey");
    $(this).addClass("activemon").removeClass("bg-lightgrey");
    if ($(this).hasClass('nomonselected')){
      $("#selectedmon").empty().append("<img class='mediumsprite' src='/static/pokemondatabase/sprites/question.png'>");
      $("#moninput").val("");
      $("#typingbox").html("-")
      $("#abilitybox").html("-")
      $("#statbox").html("<td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>")
      $("#movesbox").html("-")
    }
    else{
      selectedimgmd=$(this).find(".searchlistimg").clone()
      selectedname=$(this).find(".topname").text()
      selectedtyping=$(this).find(".searchlisttype").clone()
      selectedability=$(this).find(".searchlistability").clone()
      selectedstats=$(this).find(".topstats").html()
      selectedmoves=$(this).find(".searchlistmoves").clone()
      $("#selectedmon").html(selectedimgmd)
      $("#moninput").val(selectedname)
      $("#typingbox").html(selectedtyping)
      $("#abilitybox").html(selectedability)
      $("#statbox").html(selectedstats)
      $("#movesbox").html(selectedmoves)
    }
  })

  //loadteam
  $("#loadbutton").click(loaddraft); 

  //deleteteam
  $("#deletebutton").click(deletedraft); 

});

function savedraft() {
  draftname = $("#draftname").val();
  associatedleague = $("#associatedleague").val();
  existingdraft=$("#draftloaded").val()
  savelist = [];
  $(".topname").each(function() {
    savelist.push($(this).text());
  });
  $.post(
    "/draftplanner/savedraft",
    {
      draftname: draftname,
      associatedleague: associatedleague,
      savelist: savelist,
      existingdraft: existingdraft
    },
    function(data) {
      $("#draftloaded").val(data.response)
    }
  );
}

function loaddraft() {
  lookupdraft = $("#draftselect").val();
  if (lookupdraft != "None") {
    $.post(
      "/draftplanner/getdraft",
      {
        lookupdraft: lookupdraft
      },
      function(data) {
        $("#draftname").val(data.draftname);
        $("#associatedleague").val(data.associatedleague);
        $("#draftloaded").val(data.draftloaded);
        $(".nomonselected").remove();
        for (i = 0; i < data.lookupdraft.length; i++) {
          //alert('start')
          addMon()        
          moi=data.lookupdraft[i]
          listitem=$(".searchlistname").filter(function(){return $(this).text()==moi}).closest(".monsearchlistitem")
          selectedimgsm=listitem.find(".searchlistimg").clone()
          selectedimgmd=listitem.find(".searchlistimg").clone().removeClass('smallsprite').addClass('mediumsprite')
          selectedname=listitem.find(".searchlistname").text()
          selectedtyping=listitem.find(".searchlisttype").clone()
          selectedability=listitem.find(".searchlistability").clone()
          selectedstats=listitem.find(".statstable").html()
          selectedmoves=listitem.find(".searchlistmoves").clone()
          $("#selectedmon").html(selectedimgmd)
          $("#moninput").val(selectedname)
          $("#typingbox").html(selectedtyping)
          $("#abilitybox").html(selectedability)
          $("#statbox").html(selectedstats)
          $("#movesbox").html(selectedmoves)
          $(".activemon").html(selectedimgmd.clone()).removeClass('nomonselected')
          $(".activemon").append('<div class="topname" hidden></div><div class="toptypes" hidden></div><div class="topabilities" hidden></div><div class="topstats" hidden></div><div class="topmoves" hidden></div>')
          $(".activemon .topname").append(selectedname)
          $(".activemon .toptypes").append(selectedtyping.clone())
          $(".activemon .topabilities").append(selectedability.clone())
          $(".activemon .topstats").append(selectedstats)
          $(".activemon .topmoves").append(selectedmoves.clone())
          //alert('end')
        }
        updatedata()
      }
    );
  } else {
    alert("No draft selected!");
  }
}

function deletedraft(){
  loadeddraft = $("#draftloaded").val();
  if (loadeddraft!=''){
    $.post(
      "/draftplanner/deletedraft",
      {
        loadeddraft: loadeddraft,
      },
      function(data) {
        location.reload(true)
      }
    );
  }
}

function addMon(){
  $(".activemon").removeClass("activemon").addClass("bg-lightgrey");
  $("#topmonlist").prepend("<div class='col-1 activemon text-dark text-center border nomonselected topmon'><img class='mediumsprite' src='/static/pokemondatabase/sprites/question.png'></div>");
  $("#selectedmon").empty().append("<img class='mediumsprite' src='/static/pokemondatabase/sprites/question.png'>");
  $("#moninput").val("");
  $("#typingbox").html("-")
  $("#abilitybox").html("-")
  $("#statbox").html("<td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>")
  $("#movesbox").html("-")
}

function settodefault(){
  $("#Fire").empty().append("X")
  $("#Grass").empty().append("X")
  $("#Water").empty().append("X")
  $("#Dark").empty().append("X")
  $("#Fighting").empty().append("X")
  $("#Fairy").empty().append("X")
  $("#Electric").empty().append("X")
  $("#Ground").empty().append("X")
  $("#Poison").empty().append("X")
  $("#Dragon").empty().append("X")
  $("#Steel").empty().append("X")
  $("#Psychic").empty().append("X")
  $("#Ghost").empty().append("X")
  $("#speed_g1").empty().append("None")
  $("#speed_g2").empty().append("None")
  $("#speed_g3").empty().append("None")
  $("#speed_g4").empty().append("None")
  $("#speed_g5").empty().append("None")
  $("#speed_g6").empty().append("None")
  $("#largestspeedgap").empty().append("N/A")
  $("#StealthRock").empty().append("None")
  $("#Spikes").empty().append("None")
  $("#ToxicSpikes").empty().append("None")
  $("#StickyWeb").empty().append("None")
  $("#HazardControl").empty().append("None")
  $("#Cleric").empty().append("None")
  $("#Wish").empty().append("None")
  $("#Priority").empty().append("None")
  for (num = -2; num < 4; num++) {
    $("#Bug"+num).empty()
    $("#Dark"+num).empty()
    $("#Dragon"+num).empty()
    $("#Electric"+num).empty()
    $("#Fairy"+num).empty()
    $("#Fighting"+num).empty()
    $("#Fire"+num).empty()
    $("#Flying"+num).empty()
    $("#Ghost"+num).empty()
    $("#Grass"+num).empty()
    $("#Ground"+num).empty()
    $("#Ice"+num).empty()
    $("#Normal"+num).empty()
    $("#Poison"+num).empty()
    $("#Psychic"+num).empty()
    $("#Rock"+num).empty()
    $("#Steel"+num).empty()
    $("#Water"+num).empty()
  }
}

function updatedata(){
  settodefault()
  monnames=$(".topname")
  monspeeds=[]
  monnames.each(function(){
    moi=$(this).text()
    monjson=JSON.parse(pokemondatabase.filter(function(el){
      return moi==Object.keys(JSON.parse(el))[0]
    }))
    spriteobject=$("<img class='smallsprite searchlistimg' src='"+monjson[moi]['sprites'][spriteurl]+"'>")
    //update moves
    priority=false
    cleric=false
    hazardcontrol=false
    for (move in monjson[moi]['learnset']){
      if (move=="Stealth Rock"){
        if($("#StealthRock").text()=="None"){$("#StealthRock").empty()}
        $("#StealthRock").append(spriteobject.clone())
      }
      else if (move=="Spikes"){
        if($("#Spikes").text()=="None"){$("#Spikes").empty()}
        $("#Spikes").append(spriteobject.clone())
      }
      else if (move=="Toxic Spikes"){
        if($("#ToxicSpikes").text()=="None"){$("#ToxicSpikes").empty()}
        $("#ToxicSpikes").append(spriteobject.clone())
      }
      else if (move=="Sticky Web"){
        if($("#StickyWeb").text()=="None"){$("#StickyWeb").empty()}
        $("#StickyWeb").append(spriteobject.clone())
      }
      else if (move=="Rapid Spin"||move=="Defog"||move=="Court Change"){
        hazardcontrol=true
      }
      else if (move=="Heal Bell"||move=="Aromatherapy"){
        cleric=true
      }
      else if (move=="Wish"){
        if($("#Wish").text()=="None"){$("#Wish").empty()}
        $("#Wish").append(spriteobject.clone())
      }
      if (monjson[moi]['learnset'][move]['Priority']>0 && (monjson[moi]['learnset'][move]['Category']=="Physical" || monjson[moi]['learnset'][move]['Category']=="Special") && move!="Bide"){
        priority=true
      }
    }
    if (cleric == true){
      if($("#Cleric").text()=="None"){$("#Cleric").empty()}
      $("#Cleric").append(spriteobject.clone())
    }
    if (hazardcontrol == true){
      if($("#HazardControl").text()=="None"){$("#HazardControl").empty()}
      $("#HazardControl").append(spriteobject.clone())
    }
    if (priority == true){
      if($("#Priority").text()=="None"){$("#Priority").empty()}
      $("#Priority").append(spriteobject.clone())
    }
    //update types
    for (type in monjson[moi]['types']){
      toi=monjson[moi]['types'][type]
      if($("#"+toi).text()=="X"){$("#"+toi).empty()}
      $("#"+toi).append(spriteobject.clone())
    }
    //update speeds
    soi=monjson[moi]['basestats']['speed']
    monspeeds.push(soi)
    if (soi<31){
      if($("#speed_g1").text()=="None"){$("#speed_g1").empty()}
      $("#speed_g1").append(spriteobject.clone())
    }
    else if (soi<51){
      if($("#speed_g2").text()=="None"){$("#speed_g2").empty()}
      $("#speed_g2").append(spriteobject.clone())
    }
    else if (soi<71){
      if($("#speed_g3").text()=="None"){$("#speed_g3").empty()}
      $("#speed_g3").append(spriteobject.clone())
    }
    else if (soi<91){
      if($("#speed_g4").text()=="None"){$("#speed_g4").empty()}
      $("#speed_g4").append(spriteobject.clone())
    }
    else if (soi<111){
      if($("#speed_g5").text()=="None"){$("#speed_g5").empty()}
      $("#speed_g5").append(spriteobject.clone())
    }
    else {
      if($("#speed_g6").text()=="None"){$("#speed_g6").empty()}
      $("#speed_g6").append(spriteobject.clone())
    }
    if (monspeeds.length>1){
      monspeeds=monspeeds.sort((a, b) => a - b)
      maxdiff=0
      for (let i = 0; i < monspeeds.length-1; i++) {
        diff=monspeeds[i+1]-monspeeds[i]
        if(diff>maxdiff){maxdiff=diff}
      }
      $("#largestspeedgap").empty().append(maxdiff)
    }
    //update resistances and weaknesses
    tmu=monjson[moi]['typematchup']
    tmukeys=Object.keys(tmu)
    for (x in tmukeys){
      t=tmukeys[x]
      rw=monjson[moi]['typematchup'][t]
      $("#"+t+rw).append(spriteobject.clone())
    }
  })
}