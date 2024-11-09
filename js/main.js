$(document).ready(function(){
    $('.card-header h6').click(function() {
        $(this).find('span').toggleClass('rotate');
        $(this).toggleClass('collapsed');
    });
});
