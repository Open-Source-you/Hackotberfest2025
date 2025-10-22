$(document).ready(function () {
    AOS.init();

    $('#slide-toggle, .overlay').click(function() {
        $('.overlay').fadeToggle(50);
        $('#menu-slider').toggleClass('hide');
        $('#main-warapper').toggleClass('left');
        $('body').toggleClass('no-scroll');
    });
});
