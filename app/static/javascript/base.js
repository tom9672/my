$(document).ready(function(){
    $('.mainmenulink').click(function() {
        sessionStorage.setItem('mainmenupage', $(this).attr('href'));
        $(this).css('background-color', 'red');
    });
    
    //alert(sessionStorage.getItem("mainmenupage"))
    $('.mainmenulink').each(function(i, obj) {
        var currentpage = sessionStorage.getItem("mainmenupage"); 
        if (currentpage !== null && currentpage == $(this).attr('href') )
        {
            $(this).css('background-color', 'red');
        }
    });
    
    });