$(document).ready(function() {
    var pickdeadline = Date.UTC(pickdeadline_[0],pickdeadline_[1]-1,pickdeadline_[2],pickdeadline_[3],pickdeadline_[4])
    setInterval(function(){
        var currenttime= Date.now()
        var timeremaining=timeConversion(pickdeadline-currenttime)
        $("#timer").text(timeremaining)
    }, 1000);
})

function timeConversion(millisec) {
    if (millisec>=0){var hours = Math.floor((millisec / (1000 * 60 * 60)));}
    else {var hours = Math.ceil((millisec / (1000 * 60 * 60)));}
    millisec=Math.abs(millisec)-Math.abs(hours)*60*60*1000
    var minutes = Math.floor(((millisec) / (1000 * 60)));
    millisec=millisec-minutes*60*1000
    var seconds = Math.floor((millisec / 1000).toFixed(1));
    return hours +" hrs " + minutes + " mins " + seconds + " secs ";
}  