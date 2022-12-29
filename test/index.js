$(document).ready(function(){
    $('a').on('mousedown', stopNavigate);

    $('a').on('mouseleave', function () {
        $(window).on('beforeunload', function(){
                console.log("Im here"); 
                return 'Are you sure you want to leave?';
        });
    });
});

function stopNavigate(){   
    $(window).off('beforeunload');
}