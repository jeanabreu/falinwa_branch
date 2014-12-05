openerp.fal_easy_inventory = function(instance) {
    var QWeb = instance.web.qweb,
        _lt = instance.web._lt,
        _t = instance.web._t;

    instance.web.form.widgets.add('FalEan', 'instance.fal_easy_inventory.FalEan');
    instance.web.form.widgets.add('falname', 'instance.fal_easy_inventory.falname');
    instance.fal_easy_inventory.FalEan = instance.web.form.FieldChar.extend( {
        template: 'FalEan',
        initialize_content: function() {
            this.$el.find('input.FalEan').keyup(this.on_changing);
        },
        on_changing: function() {
                        var parent = this.getParent();
                        var qtyfield = parent.$el.find('span.falqty :first-child');
                        if (this.$el.find('input.FalEan').val().length >= 13) {
                            qtyfield.val('');
                            qtyfield.focus();
                        }
                    }
    }); 
    instance.fal_easy_inventory.falname = instance.web.form.FieldChar.extend( {
        template: 'falname',
    }); 

    instance.web.FormView.include({
        load_record: function(records) {
            var self = this;
            self._super(records);
            if(self.model == 'easy.inventory.wizard') {
                var namefield = this.$el.find('input.falname');
                if (namefield.val() != ''){
                    this.$el.find('input.FalEan').focus();
                }
            }
        },
    }); 
}