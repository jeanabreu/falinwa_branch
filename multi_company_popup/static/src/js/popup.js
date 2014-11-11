openerp.multi_company_popup = function (instance) {
    var QWeb = instance.web.qweb,
        _t = instance.web._t;
    //add popup choose company
    instance.web.Login.include({
        do_login: function (db, login, password) {
            var self = this;
            self.hide_error();
            self.$(".oe_login_pane").fadeOut("slow");
            return this.session.session_authenticate(db, login, password).then(function() {
                self.remember_last_used_database(db);
                if (self.has_local_storage && self.remember_credentials) {
                    localStorage.setItem(db + '|last_login', login);
                }
                //self.trigger('login_successful');
                // and call `resolve` on the deferred object, once you're done
                //todo
                self.action_manager = new instance.web.ActionManager(self);
                var func = new instance.web.Model("ir.actions.act_window").get_func("for_xml_id");
                var home_action = func('multi_company_popup', 'action_popup_after_login_config').then(function(result){
                    if (result.id){
                        self.user_action_id = result.id;   
                        self.action_manager.do_action(self.user_action_id, {'clear_breadcrumbs': true});
                    }
                })
            }, function () {
                self.$(".oe_login_pane").fadeIn("fast", function() {
                    self.show_error(_t("Invalid username or password"));
                });
            });
        }
    });
}