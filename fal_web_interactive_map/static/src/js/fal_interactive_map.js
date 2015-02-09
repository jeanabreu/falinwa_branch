  function hideMarkDescription(id){
    document.getElementById(id).style.display = "none";
  };
  
  function showMarkDescription(mark_id, des_id){
    var des_top = parseInt(document.getElementById(mark_id).offsetTop, 10) - 129 + 'px';
    var des_left = parseInt(document.getElementById(mark_id).offsetLeft, 10) - 218 + 'px' ;
    document.getElementById(des_id).style.display = "block";
    document.getElementById(des_id).style.top = des_top;
    document.getElementById(des_id).style.left = des_left;
  };

(function () {
    'use strict';
    var website = openerp.website;  
    console.log(website.snippet);
    console.log(website.snippet.options.slider);
    website.snippet.options.slider.include({
        start : function () {
            this._super();
            this.$target.carousel({interval: 1});
        },    
    }); 
})();