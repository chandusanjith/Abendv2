
    $(document).ready( function(){
         myFunction();
    });
    function myFunction() {
        if(sessionStorage.getItem('mode') === 'dark')
        {
            $('body').addClass('dark');
            $('footer').addClass('dark');
        }
        else
        {
            $('body').removeClass('dark');
            $('footer').removeClass('dark');
        }
        /*sessionStorage.getItem('mode') === 'dark' ? document.querySelector('body').classList.add('dark') : document.querySelector('body').classList.remove('dark');*/
        /*sessionStorage.getItem('mode') === 'dark' ? document.querySelector('footer').classList.add('dark') : document.querySelector('footer').classList.remove('dark');*/
    }
    function myDark() {
        sessionStorage.setItem('mode', (sessionStorage.getItem('mode') || 'dark') === 'dark' ? 'light' : 'dark');
        myFunction();
    }

        document.addEventListener("DOMContentLoaded", function(){
	$('.preloader-background').delay(500).fadeOut('slow');

	$('.preloader-wrapper')
		.delay(500)
		.fadeOut();
});
