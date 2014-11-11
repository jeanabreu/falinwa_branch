openerp.color_company = function (instance) {
    var QWeb = instance.web.qweb,
        _t = instance.web._t;
    
    //add company color
    instance.web.WebClient.include({
        show_application: function() {
            var self = this;
            self.update_color();
            this._super.apply(this, arguments);
        },
        update_color: function() {
            var self = this;
            var funct = new instance.web.Model("res.users").get_func("read")(this.session.uid, ["company_id"]).then(function(res) {
                var funct1 = new instance.web.Model("res.company").get_func("read")(res['company_id'][0], ["color"]).then(function(rest) {
                    if(rest['color']){
                        self.$('.oe_leftbar').attr('style', 'background:'+rest['color']+';');
                    }
                })
            })
        },
    });
}