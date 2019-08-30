$(document).ready(function() {
  //add mon
  $("#addmon").click(function() {
    $(".activemon")
      .removeClass("activemon")
      .addClass("bg-lightgrey");
    $("#topmonlist").prepend(
      "<div class='col-1 activemon text-dark text-center border nomonselected'><img class='mediumsprite' src='https://play.pokemonshowdown.com/sprites/xyani/unown-question.gif'></div>"
    );
    $("#moninput").val("");
    $("#selectedmon")
      .empty()
      .append(
        "<img class='mediumsprite' src='https://play.pokemonshowdown.com/sprites/xyani/unown-question.gif'>"
      );
    //select nomonselected
    $(".nomonselected").click(function() {
      $(".activemon")
        .addClass("bg-lightgrey")
        .removeClass("activemon");
      $(this)
        .removeClass("bg-lightgrey")
        .addClass("activemon");
      $("#moninput").val("");
      $("#selectedmon")
        .empty()
        .append(
          "<img class='mediumsprite' src='https://play.pokemonshowdown.com/sprites/xyani/unown-question.gif'>"
        );
    });
  });

  //searchbox
  $("#moninput").keyup(function() {
    lookupmon = $("#moninput").val();
    $.post(
      "/draftplanner/getmon",
      {
        lookupmon: lookupmon
      },
      function(data) {
        $("#monsearchlist").empty();
        for (i = 0; i < data.length; i++) {
          $("#monsearchlist").append(
            "<div class='col-12 border monsearchlistitem'>" +
              data[i].fields.pokemon +
              "</div>"
          );
        }
        //select list mon
        $(".monsearchlistitem").click(function() {
          selectmonfromlist($(this).text());
          $("#monsearchlist").empty();
          $(".activemon").empty();
          updateactivemon($(this).text());
          updatedata()
          $(".activemon").removeClass("nomonselected").addClass("monselected")
          //select loaded mon
          $(".monselected").click(function() {
            $(".activemon")
              .addClass("bg-lightgrey")
              .removeClass("activemon");
            $(this)
              .removeClass("bg-lightgrey")
              .addClass("activemon");
            selectmonfromlist(
              $(this)
                .children()
                .text()
            );
            updatedata()
          });
        });
      }
    );
  });

  //loadteam
  $("#loadbutton").click(function() {
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
          $(".monselected").remove();
          for (i = 0; i < data.lookupdraft.length; i++) {
            x = $("#topmonlist").prepend(
              "<div class='col-1 bg-lightgrey text-dark text-center border monselected'><img class='mediumsprite' src='https://play.pokemonshowdown.com/sprites/xyani/" +
                data.lookupdraft[i]
                  .toLowerCase()
                  .replace(" ", "")
                  .replace(".", "")
                  .replace(":", "")
                  .replace("%", "")
                  .replace("mega-,mega")
                  .replace("nidoran-m,nidoran")
                  .replace("o-o,oo")
                  .replace("dusk-mane,duskmane")
                  .replace("dawn-wings", "dawnwings") +
                ".gif'><div class='saveidentifier' hidden>" +
                data.lookupdraft[i] +
                "</div></div>"
            );
            if (i == 0) {
              $("#moninput").val(data.lookupdraft[i]);
              $(".monselected")
                .removeClass("bg-lightgrey")
                .addClass("activemon");
              $(".selectedmon").empty();
              selectmonfromlist(data.lookupdraft[i]);
            }
          }
          //select loaded mon
          $(".monselected").click(function() {
            $(".activemon")
              .addClass("bg-lightgrey")
              .removeClass("activemon");
            $(this)
              .removeClass("bg-lightgrey")
              .addClass("activemon");
            selectmonfromlist(
              $(this)
                .children()
                .text()
            );
          });
          updatedata()
        }
      );
    } else {
      alert("No draft selected!");
    }
  });

  //saveteam
  setInterval(function() {
    draftname = $("#draftname").val();
    associatedleague = $("#associatedleague").val();
    existingdraft=$("#draftloaded").val()
    savelist = [];
    $(".saveidentifier").each(function() {
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
  },10000);

  //deleteteam
  $("#deletebutton").click(function() {
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
  });
});

function selectmonfromlist(name) {
  $("#moninput").val(name);
  $("#selectedmon").empty();
  $("#selectedmon").append(
    "<img class='mediumsprite' src='https://play.pokemonshowdown.com/sprites/xyani/" +
      name
        .toLowerCase()
        .replace(" ", "")
        .replace(".", "")
        .replace(":", "")
        .replace("%", "")
        .replace("mega-,mega")
        .replace("nidoran-m,nidoran")
        .replace("o-o,oo")
        .replace("dusk-mane,duskmane")
        .replace("dawn-wings", "dawnwings") +
      ".gif'>"
  );
}
function updateactivemon(name) {
    $(".activemon").append(
    "<img class='mediumsprite' src='https://play.pokemonshowdown.com/sprites/xyani/" +
      name
        .toLowerCase()
        .replace(" ", "")
        .replace(".", "")
        .replace(":", "")
        .replace("%", "")
        .replace("mega-,mega")
        .replace("nidoran-m,nidoran")
        .replace("o-o,oo")
        .replace("dusk-mane,duskmane")
        .replace("dawn-wings", "dawnwings") +
      ".gif'>"
  );
  $(".activemon").append("<div class='saveidentifier' hidden>" +
  name +
  "</div>")
}

function updatedata() {
    savelist = [];
    $(".saveidentifier").each(function() {
      savelist.push($(this).text());
    });
    $.post(
      "/draftplanner/updatedata",
      {
        savelist: savelist,
      },
      function(data) {
        settodefault()
        for (i = 0; i < data.response.length; i++) {
          if (data.response[i][2]=="Y"){
          appendsprite(data.response[i][0],data.response[i][1])
          }
          else{
            $(data.response[i][0]).empty().append(data.response[i][1])
          }
        }
      }
    );
}

function appendsprite(identifier,name){
  if ($(identifier).html()=="None" || $(identifier).html()=="X"){
  $(identifier).empty()
  }
  $(identifier).append(
    "<img class='smallsprite' src='https://play.pokemonshowdown.com/sprites/xyani/" +
      name
        .toLowerCase()
        .replace(" ", "")
        .replace(".", "")
        .replace(":", "")
        .replace("%", "")
        .replace("mega-,mega")
        .replace("nidoran-m,nidoran")
        .replace("o-o,oo")
        .replace("dusk-mane,duskmane")
        .replace("dawn-wings", "dawnwings") +
      ".gif'>"
  );
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
  $("#Defog").empty().append("None")
  $("#RapidSpin").empty().append("None")
  $("#Cleric").empty().append("None")
  $("#Wish").empty().append("None")
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