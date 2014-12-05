openerp.fal_bom_reader = function(instance) {
    var QWeb = instance.web.qweb,
        _lt = instance.web._lt,
        _t = instance.web._t;
    
    instance.web.TreeView.include({        
        getdata: function (id, children_ids) {
            var self = this;
            if(this.dataset.model != 'mrp.bom'){
                this._super.apply(this, arguments);
            } else {
                self.dataset.read_ids(children_ids, this.fields_list()).done(function(records) {
                    _(records).each(function (record) {
                        self.records[record.id] = record;
                    });
                    var $curr_node = self.$el.find('#treerow_' + id);
                    var children_rows = QWeb.render('TreeView.rows', {
                        'records': records,
                        'children_field': self.children_field,
                        'fields_view': self.fields_view.arch.children,
                        'fields': self.fields,
                        'level': $curr_node.data('level') || 0,
                        'render': instance.web.format_value,
                        'color_for': self.color_for,
                        'row_parent_id': id
                    });
                    if ($curr_node.length) {
                        $curr_node.addClass('oe_open');
                        $curr_node.after(children_rows);
                    } else {
                        self.$el.find('tbody').html(children_rows);
                    }
                    child_rows = self.$el.find("#"+$(children_rows).attr('id'))
                    self.expand_childrens(children_rows);
                });
            }
        },
        expand_childrens: function(children_rows) {
            var self = this;
            _.each($(children_rows), function(row) {
                $row = self.$el.find("#"+$(row).attr('id'))
                if(!$row.hasClass('oe_open')) {
                    $row.children().trigger('click');
                }
            });
        },
    });
    
    instance.web.form.widgets.add('FalEanBomReader', 'instance.fal_bom_reader.FalEanBomReader');
    instance.fal_bom_reader.FalEanBomReader = instance.web.form.FieldChar.extend( {
        template: 'FalEanBomReader',
        initialize_content: function() {
            this.$el.find('input.FalEanBomReader').keyup(this.on_changing);
        },
        on_changing: function() {
                        var parent = this.getParent();
                        if (this.$el.find('input.FalEanBomReader').val().length >= 13) {
                            parent.$buttons.find('button.bombutton').trigger('click');
                        }
                    }
    }); 
}