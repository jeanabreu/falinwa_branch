(function () {
    'use strict';
    
    var website = openerp.website;

    
    website.snippet.animationRegistry.slider.include({
        start: function () {
            this.$target.carousel({interval: 4000});
        },
    })
    
})();
