$(document).ready(function() {
    selectoptions=$(".logoselect option")
    selectoptions.each(function(){
        imageurl=$(this).text()
        $(this).css("background-image","url(" + imageurl + ")")

    })

    $('.logoselect').append('<div class="button"></div>');    
    $('.logoselect').append('<ul class="select-list"></ul>');    
    
    //for each select
    $('.logoselect select option').each(function() {  
        var bg = $(this).css('background-image');    
        $('.select-list').append('<li class="clsAnchor"><span value="' + $(this).val() + '" class="' + $(this).attr('class') + '" style=background-image:' + bg + '><span hidden>' + $(this).text() + '</span></span></li>');   
    });    

    $('.logoselect .button').html('<span style=background-image:' + $('.logoselect select').find(':selected').css('background-image') + '><span hidden>' + $('.logoselect select').find(':selected').text() + '</span><a href="javascript:void(0);" class="select-list-link text-dark">▼</a></span>');   
    $('.logoselect ul li').each(function() {   
    if ($(this).find('span').text() == $('.logoselect select').find(':selected').text()) {  
        $(this).addClass('active');       
    }      
    });   
    //on selecting image  
    $('.logoselect .select-list span').on('click', function()
    {          
        var dd_text = $(this).text();  
        var dd_img = $(this).css('background-image'); 
        var dd_val = $(this).attr('value');   
        $('.logoselect .button').html('<span style=background-image:' + dd_img + '><span hidden>' + dd_text + '</span><a href="javascript:void(0);" class="select-list-link text-dark">▼</a></span>');      
        $('.logoselect .select-list span').parent().removeClass('active');    
        $(this).parent().addClass('active');     
        $('.logoselect select[name=logo_0]').val( dd_val ); 
        $('.logoselect .select-list li').slideUp();     
        });       
        $('.logoselect .button').on('click','a.select-list-link', function()
        {      
        $('.logoselect ul li').slideToggle();  
    });     
});