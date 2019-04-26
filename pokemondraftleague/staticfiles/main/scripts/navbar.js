document.addEventListener('DOMContentLoaded', function() {
    dropdowns=document.querySelectorAll('.dropbtn')
    dropdowns.forEach(function(element) {
        element.onclick = function() {
            element.nextElementSibling.classList.toggle("show");
        };
    });
});
