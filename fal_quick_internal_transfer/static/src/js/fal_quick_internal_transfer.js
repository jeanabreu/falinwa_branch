openerp.fal_quick_internal_transfer = function(instance) {
    var QWeb = instance.web.qweb,
        _lt = instance.web._lt,
        _t = instance.web._t;

    instance.web.form.widgets.add('FalEan', 'instance.fal_quick_internal_transfer.FalEan');
    instance.web.form.widgets.add('FalSourceEan', 'instance.fal_quick_internal_transfer.FalSourceEan');
    instance.web.form.widgets.add('FalDestinationEan', 'instance.fal_quick_internal_transfer.FalDestinationEan');
    instance.web.form.widgets.add('falname', 'instance.fal_quick_internal_transfer.falname');
    
    instance.fal_quick_internal_transfer.FalEan = instance.web.form.FieldChar.extend( {
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
    
    instance.fal_quick_internal_transfer.FalSourceEan = instance.web.form.FieldChar.extend( {
        template: 'FalSourceEan',
        initialize_content: function() {
            this.$el.find('input.FalSourceEan').keyup(this.on_changing);
        },
        on_changing: function() {
                        var parent = this.getParent();
                        var destEanfield = parent.$el.find('input.FalDestinationEan');
                        if (this.$el.find('input.FalSourceEan').val().length >= 13) {
                            destEanfield.val('');
                            destEanfield.focus();
                        }
                    }
    });

    instance.fal_quick_internal_transfer.FalDestinationEan = instance.web.form.FieldChar.extend( {
        template: 'FalDestinationEan',
    });
    
    instance.fal_quick_internal_transfer.falname = instance.web.form.FieldChar.extend( {
        template: 'falname',
    }); 

    instance.web.FormView.include({
        load_record: function(records) {
            var self = this;
            self._super(records);
            if(self.model == 'quick.internal.transfer.wizard') {
                    this.$el.find('input.FalEan').focus();
            }
        },
    }); 
}