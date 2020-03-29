$(document).ready(function() {
  //configure searchlist
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading d-none'><div class='col-12'>Pokemon</div></div>")
  for (x in pokemondatabase){
    jsonitem=JSON.parse(pokemondatabase[x])
    itemname=Object.keys(jsonitem)[0]
    outer=$("<div class='row p-1 border border-dark bg-lightgrey text-dark monsearchlistitem d-none'></div>")
    outer.append("<div class='col-2 d-flex justify-content-center align-items-center text-center'><img class='smallsprite searchlistimg' src='"+jsonitem[itemname]['sprites'][spriteurl]+"'><span class='searchlistname'>"+itemname+"</span><span class='listpts d-none'> (<span class='itemcost'></span> pts)</span></div>")
    inner=$("<div class='col-1 d-flex justify-content-center align-items-center'></div>")
    for (type in jsonitem[itemname]['types']){
      inner.append("<div><img class='searchlisttype' src='/static/pokemondatabase/sprites/types/"+jsonitem[itemname]['types'][type]+".png'></div>")
      outer.addClass("type-"+jsonitem[itemname]['types'][type].replace(/ /g,""))
    }
    outer.append(inner)
    inner=$("<div class='col-3 text-center my-auto'></div>")
    inner.append("<small class='searchlistability'>"+jsonitem[itemname]['abilities'].join(", ")+"</small>")
    for (ability in jsonitem[itemname]['abilities']){
      outer.addClass("ability-"+jsonitem[itemname]['abilities'][ability].replace(/ /g,""))
    }
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
      outer.addClass("move-"+learnset[move].replace(/ /g,""))
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
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading np-searchheading d-none'><div class='col-12'>Types</div></div>")
  for (x in typelist){
    $("#monsearchlist").append("<div class='row p-1 border border-dark bg-lightgrey text-dark d-none filteritem filtertype'><div class='col-12'>"+typelist[x]+"</div></div>")
  }
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading np-searchheading d-none'><div class='col-12'>Abilities</div></div>")
  for (x in abilitylist){
    $("#monsearchlist").append("<div class='row p-1 border border-dark bg-lightgrey text-dark d-none filteritem filterability'><div class='col-12'>"+abilitylist[x]+"</div></div>")
  }
  $("#monsearchlist").append("<div class='row p-1 border border-dark bg-dark text-light searchheading np-searchheading d-none'><div class='col-12'>Moves</div></div>")
  for (x in movelist){
    $("#monsearchlist").append("<div class='row p-1 border border-dark bg-lightgrey text-dark d-none filteritem filtermove'><div class='col-12'>"+movelist[x]+"</div></div>")
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
    $(".activemon").append('<div class="topname" hidden></div><div class="toptypes" hidden></div><div class="topabilities" hidden></div><div class="topstats" hidden></div><div class="topmoves" hidden></div><div class="toppoints d-none">(<span class="toppointvalue"></span> pts)</div>')
    $(".activemon .topname").append(selectedname)
    $(".activemon .toptypes").append(selectedtyping.clone())
    $(".activemon .topabilities").append(selectedability.clone())
    $(".activemon .topstats").append(selectedstats)
    $(".activemon .topmoves").append(selectedmoves.clone())
    $(".searchheading").addClass('d-none')
    $(".filteritem").addClass('d-none')
    $(".monsearchlistitem").addClass('d-none')
    $(".activefilter").remove()
    savedraft()
    updatedata()
    addleaguetiering()
  })

  //click filteritam
  $(".filteritem").click(function() {
    filtertext=$(this).find(".col-12").text()
    if ($(this).hasClass('filtertype')){
    $("#filterarea").append("<span class='border border-secondary rounded activefilter filtertype mr-1'><span class='filtertext'>"+filtertext+"</span> <span class='activefilterdelete'>ⓧ</span></span>")
    }
    else if ($(this).hasClass('filterability')){
      $("#filterarea").append("<span class='border border-secondary rounded activefilter filterability mr-1'><span class='filtertext'>"+filtertext+"</span> <span class='activefilterdelete'>ⓧ</span></span>")
    }
    else if ($(this).hasClass('filtermove')){
      $("#filterarea").append("<span class='border border-secondary rounded activefilter filtermove mr-1'><span class='filtertext'>"+filtertext+"</span> <span class='activefilterdelete'>ⓧ</span></span>")
    }
    $(".np-searchheading").addClass('d-none')
    $(".filteritem").addClass('d-none')
    $("#moninput").val("")
    filterlist()
  })

  //delete filteritem
  $("span").on('click','.activefilterdelete',function(){
    $(this).closest(".activefilter").remove()
    filterlist()
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
    $(".filteritem").each(function() {
      lu=String(lookup).toLowerCase()
      item=$(this)
      clickedtext=item.find(".col-12").text()
      if (clickedtext.toLowerCase().includes(lu)){
        item.removeClass('d-none')
      }
      else{
        item.addClass('d-none')
      }
      $(".activefilter").each(function(){
        if ($(this).find(".filtertext").text()==clickedtext){
          item.addClass('d-none')
        }
      })
    })
    }
    else{
      $(".searchheading").addClass('d-none')
      $(".monsearchlistitem").addClass('d-none')
      $(".filteritem").addClass('d-none')
    }
    $(".filtered").addClass('d-none')
  })

  //addmon
  $("#addmon").click(addMon)

  //addmon
  $("#showcriteria").click(function(){
    if ($("#showcriteria").text()=="Show Criteria"){
      $("#criteriatable").removeClass("d-none")
      $("#showcriteria").text("Hide Criteria")
    }
    else{
      $("#criteriatable").addClass("d-none")
      $("#showcriteria").text("Show Criteria")
    }
  })

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

  //delete item
  $("#deleteitembutton").click(deleteitem); 

  //loadteam
  $("#draftselect").change(loaddraft); 

  //deleteteam
  $("#deletebutton").click(deletedraft); 

  //change associated league
  $("#associatedleague").change(addleaguetiering)

});

function addleaguetiering(){
  al_value=$("#associatedleague").val()
  $(".Banned").removeClass("Banned")
  $(".TopBanned").removeClass("TopBanned")
  $(".toppoints").html("(<span class='toppointvalue'></span> pts)")
  $(".listpts").html(" (<span class='itemcost'></span> pts)")
  if (al_value=="None"){
    $("#availablepoints").addClass("d-none")
    $(".listpts").addClass("d-none")
    $(".toppoints").addClass("d-none")
  }
  else {
    $("#availablepoints").removeClass("d-none")
    $(".listpts").removeClass("d-none")
    $(".toppoints").removeClass("d-none")
    associatedleague = $("#associatedleague").val();
    $.post(
      "/draftplanner/gettiers",
      {
        associatedleague: associatedleague,
      },
      function(data) {
        $("#totalpoints").text(data.draftbudget)
        tierlist=data.tiers
        for (x in tierlist){
          mon=tierlist[x][0]
          tiername=tierlist[x][1]
          points=tierlist[x][2]
          listitem=$(".monsearchlistitem").filter(function(){return $(this).find(".searchlistname").text()==mon})
          if (tiername=="Banned"){
            listitem.addClass("Banned")
          }
          listitem.find(".itemcost").text(points)
          $(".Banned").find(".listpts").text("(Banned)")
          listitem=$(".topmon").filter(function(){return $(this).find(".topname").text()==mon})
          if (tiername=="Banned"){
            listitem.addClass("TopBanned")
          }
          listitem.find(".toppointvalue").text(points)
          $(".TopBanned").find(".toppoints").text("(Banned)")
        }
        pointsremaining=data.draftbudget
        (".toppointvalue").each(function(){
          pointsremaining=pointsremaining-parseInt($(this).text())
        })
        $("#remainingpoints").text(pointsremaing)
      }
    );
  }
  savedraft()
}

function filterlist(){
  $(".monsearchlistitem").removeClass('d-none')
  if ($(".activefilter").length>0){
    $(".monsearchlistitem").addClass('filtered')
  }
  else{
    $(".monsearchlistitem").removeClass('filtered')
  }
  requiredclass=[]
  $(".activefilter").each(function(){
    if ($(this).hasClass("filtertype")){
      requiredclass.push(".type-"+$(this).find(".filtertext").text().replace(/ /g,""))
    }
    else if ($(this).hasClass("filterability")){
      requiredclass.push(".ability-"+$(this).find(".filtertext").text().replace(/ /g,""))
    }
    else if ($(this).hasClass("filtermove")){
      requiredclass.push(".move-"+$(this).find(".filtertext").text().replace(/ /g,""))
    }
  })
  $(".monsearchlistitem"+requiredclass.join("")).removeClass('filtered')
  $(".filtered").addClass("d-none")
}


function updatescore(){
  score=0
  //typing bonuses
  if($("#Grass img").length>0){grass=2}else{grass=0}
  if($("#Fire img").length>0){fire=2}else{fire=0}
  if($("#Water img").length>0){water=2}else{water=0}
  if(grass+fire+water==6){gfwbonus=2}else{gfwbonus=0}
  score=score+grass+fire+water+gfwbonus
  if($("#Psychic img").length>0){psychic=2}else{psychic=0}
  if($("#Fighting img").length>0){fighting=2}else{fighting=0}
  if($("#Dark img").length>0){dark=2}else{dark=0}
  if(psychic+fighting+dark==6){pfdbonus=2}else{pfdbonus=0}
  score=score+psychic+fighting+dark+pfdbonus
  if($("#Dragon img").length>0){dragon=2}else{dragon=0}
  if($("#Fairy img").length>0){fairy=2}else{fairy=0}
  if($("#Steel img").length>0){steel=2}else{steel=0}
  if(dragon+fairy+steel==6){dfsbonus=2}else{dfsbonus=0}
  score=score+dragon+fairy+steel+dfsbonus
  if($("#Electric img").length>0){electric=2}else{electric=0}
  if($("#Ground img").length>0){ground=2}else{ground=0}
  if($("#Poison img").length>0){poison=2}else{poison=0}
  if(electric+ground+poison==6){egpbonus=1}else{egpbonus=0}
  score=score+electric+ground+poison+egpbonus
  if($("#Ghost img").length>0){ghost=2}else{ghost=0}
  score=score+ghost
  //speed tier bonus
  if($("#speed_g1 img").length>0){sg1=2}else{sg1=0}
  if($("#speed_g2 img").length>0){sg2=2}else{sg2=0}
  if($("#speed_g3 img").length>0){sg3=2}else{sg3=0}
  if($("#speed_g4 img").length>0){sg4=2}else{sg4=0}
  if($("#speed_g5 img").length>0){sg5=2}else{sg5=0}
  if($("#speed_g6 img").length>0){sg6=3}else{sg6=0}
  if(parseInt($("#largestspeedgap").text())<21){speedgap=3}else{speedgap=0}
  score=score+sg1+sg2+sg3+sg4+sg5+sg6+speedgap
  //moves bonus
  stealthrock=$("#StealthRock img").length*2
  if($("#StealthRock img").length>2){stealthrock=4}
  if(($("#Spikes img").length+$("#ToxicSpikes img").length+$("#StickyWeb img").length)>0){s_ts_sw=2}else{s_ts_sw=0}
  removal=$("#HazardControl img").length*2
  if($("#HazardControl img").length>2){removal=4}
  if($("#Cleric img").length>0){cleric=2}else{cleric=0}
  if($("#Wish img").length>0){wish=2}else{wish=0}
  if($("#Priority img").length>2){priority=1}else{priority=0}
  score=score+stealthrock+s_ts_sw+removal+cleric+wish+priority
  //resists bonus
  if(($("#Bug1 img").length+$("#Bug2 img").length+$("#Bug3 img").length)>1){bug=1}else{bug=0}
  if(($("#Dark1 img").length+$("#Dark2 img").length+$("#Dark3 img").length)>1){dark=1}else{dark=0}
  if(($("#Dragon1 img").length+$("#Dragon2 img").length+$("#Dragon3 img").length)>1){dragon=1}else{dragon=0}
  if(($("#Electric1 img").length+$("#Electric2 img").length+$("#Electric3 img").length)>1){electric=1}else{electric=0}
  if(($("#Fairy1 img").length+$("#Fairy2 img").length+$("#Fairy3 img").length)>1){fairy=1}else{fairy=0}
  if(($("#Fighting1 img").length+$("#Fighting2 img").length+$("#Fighting3 img").length)>1){fighting=1}else{fighting=0}
  if(($("#Fire1 img").length+$("#Fire2 img").length+$("#Fire3 img").length)>1){fire=1}else{fire=0}
  if(($("#Flying1 img").length+$("#Flying2 img").length+$("#Flying3 img").length)>1){flying=1}else{flying=0}
  if(($("#Ghost1 img").length+$("#Ghost2 img").length+$("#Ghost3 img").length)>1){ghost=1}else{ghost=0}
  if(($("#Grass1 img").length+$("#Grass2 img").length+$("#Grass3 img").length)>1){grass=1}else{grass=0}
  if(($("#Ground1 img").length+$("#Ground2 img").length+$("#Ground3 img").length)>1){ground=1}else{ground=0}
  if(($("#Ice1 img").length+$("#Ice2 img").length+$("#Ice3 img").length)>1){ice=1}else{ice=0}
  if(($("#Normal1 img").length+$("#Normal2 img").length+$("#Normal3 img").length)>1){normal=1}else{normal=0}
  if(($("#Poison1 img").length+$("#Poison2 img").length+$("#Poison3 img").length)>1){poison=1}else{poison=0}
  if(($("#Psychic1 img").length+$("#Psychic2 img").length+$("#Psychic3 img").length)>1){psychic=1}else{psychic=0}
  if(($("#Rock1 img").length+$("#Rock2 img").length+$("#Rock3 img").length)>1){rock=1}else{rock=0}
  if(($("#Steel1 img").length+$("#Steel2 img").length+$("#Steel3 img").length)>1){steel=1}else{steel=0}
  if(($("#Water1 img").length+$("#Water2 img").length+$("#Water3 img").length)>1){water=1}else{water=0}
  score=score+bug+dark+dragon+electric+fairy+fighting+fire+flying+ghost+grass+ground+ice+normal+poison+psychic+rock+steel+water
  //resists-weak bonus
  if(($("#Bug1 img").length+$("#Bug2 img").length+$("#Bug3 img").length-$("#Bug-1 img").length-$("#Bug-2 img").length)>=0){bug=1}else{bug=0}
  if(($("#Dark1 img").length+$("#Dark2 img").length+$("#Dark3 img").length-$("#Dark-1 img").length-$("#Dark-2 img").length)>=0){dark=1}else{dark=0}
  if(($("#Dragon1 img").length+$("#Dragon2 img").length+$("#Dragon3 img").length-$("#Dragon-1 img").length-$("#Dragon-2 img").length)>=0){dragon=1}else{dragon=0}
  if(($("#Electric1 img").length+$("#Electric2 img").length+$("#Electric3 img").length-$("#Electric-1 img").length-$("#Electric-2 img").length)>=0){electric=1}else{electric=0}
  if(($("#Fairy1 img").length+$("#Fairy2 img").length+$("#Fairy3 img").length-$("#Fairy-1 img").length-$("#Fairy-2 img").length)>=0){fairy=1}else{fairy=0}
  if(($("#Fighting1 img").length+$("#Fighting2 img").length+$("#Fighting3 img").length-$("#Fighting-1 img").length-$("#Fighting-2 img").length)>=0){fighting=1}else{fighting=0}
  if(($("#Fire1 img").length+$("#Fire2 img").length+$("#Fire3 img").length-$("#Fire-1 img").length-$("#Fire-2 img").length)>=0){fire=1}else{fire=0}
  if(($("#Flying1 img").length+$("#Flying2 img").length+$("#Flying3 img").length-$("#Flying-1 img").length-$("#Flying-2 img").length)>=0){flying=1}else{flying=0}
  if(($("#Ghost1 img").length+$("#Ghost2 img").length+$("#Ghost3 img").length-$("#Ghost-1 img").length-$("#Ghost-2 img").length)>=0){ghost=1}else{ghost=0}
  if(($("#Grass1 img").length+$("#Grass2 img").length+$("#Grass3 img").length-$("#Grass-1 img").length-$("#Grass-2 img").length)>=0){grass=1}else{grass=0}
  if(($("#Ground1 img").length+$("#Ground2 img").length+$("#Ground3 img").length-$("#Ground-1 img").length-$("#Ground-2 img").length)>=0){ground=1}else{ground=0}
  if(($("#Ice1 img").length+$("#Ice2 img").length+$("#Ice3 img").length-$("#Ice-1 img").length-$("#Ice-2 img").length)>=0){ice=1}else{ice=0}
  if(($("#Normal1 img").length+$("#Normal2 img").length+$("#Normal3 img").length-$("#Normal-1 img").length-$("#Normal-2 img").length)>=0){normal=1}else{normal=0}
  if(($("#Poison1 img").length+$("#Poison2 img").length+$("#Poison3 img").length-$("#Poison-1 img").length-$("#Poison-2 img").length)>=0){poison=1}else{poison=0}
  if(($("#Psychic1 img").length+$("#Psychic2 img").length+$("#Psychic3 img").length-$("#Psychic-1 img").length-$("#Psychic-2 img").length)>=0){psychic=1}else{psychic=0}
  if(($("#Rock1 img").length+$("#Rock2 img").length+$("#Rock3 img").length-$("#Rock-1 img").length-$("#Rock-2 img").length)>=0){rock=1}else{rock=0}
  if(($("#Steel1 img").length+$("#Steel2 img").length+$("#Steel3 img").length-$("#Steel-1 img").length-$("#Steel-2 img").length)>=0){steel=1}else{steel=0}
  if(($("#Water1 img").length+$("#Water2 img").length+$("#Water3 img").length-$("#Water-1 img").length-$("#Water-2 img").length)>=0){water=1}else{water=0}
  score=score+bug+dark+dragon+electric+fairy+fighting+fire+flying+ghost+grass+ground+ice+normal+poison+psychic+rock+steel+water
  $("#draftscore").text(score)
  console.log(score)
}

function deleteitem(){
  $(".activemon").remove()
  $(".topmon").first().addClass("activemon")
  am=$(".activemon")
  if (am.hasClass('nomonselected')){
    $("#selectedmon").empty().append("<img class='mediumsprite' src='/static/pokemondatabase/sprites/question.png'>");
    $("#moninput").val("");
    $("#typingbox").html("-")
    $("#abilitybox").html("-")
    $("#statbox").html("<td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>")
    $("#movesbox").html("-")
  }
  else{
    selectedimgmd=am.find(".searchlistimg").clone()
    selectedname=am.find(".topname").text()
    selectedtyping=am.find(".searchlisttype").clone()
    selectedability=am.find(".searchlistability").clone()
    selectedstats=am.find(".topstats").html()
    selectedmoves=am.find(".searchlistmoves").clone()
    $("#selectedmon").html(selectedimgmd)
    $("#moninput").val(selectedname)
    $("#typingbox").html(selectedtyping)
    $("#abilitybox").html(selectedability)
    $("#statbox").html(selectedstats)
    $("#movesbox").html(selectedmoves)
  }
  savedraft()
  updatedata()
  addleaguetiering()
}

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
        $(".topmon").remove();
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
          $(".activemon").append('<div class="topname" hidden></div><div class="toptypes" hidden></div><div class="topabilities" hidden></div><div class="topstats" hidden></div><div class="topmoves" hidden></div><div class="toppoints d-none">(<span class="toppointvalue"></span> pts)</div>')
          $(".activemon .topname").append(selectedname)
          $(".activemon .toptypes").append(selectedtyping.clone())
          $(".activemon .topabilities").append(selectedability.clone())
          $(".activemon .topstats").append(selectedstats)
          $(".activemon .topmoves").append(selectedmoves.clone())
          //alert('end')
        }
        updatedata()
        addleaguetiering()
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
  updatescore()
}