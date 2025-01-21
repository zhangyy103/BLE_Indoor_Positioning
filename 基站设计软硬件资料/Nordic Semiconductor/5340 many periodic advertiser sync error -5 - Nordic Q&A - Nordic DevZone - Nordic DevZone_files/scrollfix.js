(function ($, global) {
    
     var api = {
         scrollStop: function(callback, refresh) {
            if (!callback || typeof callback !== 'function') return;
            let isScrolling;
            global.addEventListener('scroll', function (event) {
                global.clearTimeout(isScrolling);
                isScrolling = setTimeout(callback, refresh);
            }, false);
        }
     }

    $.fourroads = $.fourroads || {};
    $.fourroads.ui = $.fourroads.ui || {};
    $.fourroads.ui.widgets = $.fourroads.ui.widgets || {};
    $.fourroads.ui.widgets.scrollfix = api;
})(jQuery, window);
