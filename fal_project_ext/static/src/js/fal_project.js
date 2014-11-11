openerp.fal_project_ext = function(openerp) {
    openerp.web_kanban.KanbanRecord.include({
        on_card_clicked: function() {
            if(this.$('.oe_fal_not_in')[0]){
                if(this.$el.find('.oe_kanban_global_click_edit').size()>0)
                    this.do_action_edit();
                else
                    this.do_action_open();
            } else {
                this._super.apply(this, arguments);
            }
        },
    });
};