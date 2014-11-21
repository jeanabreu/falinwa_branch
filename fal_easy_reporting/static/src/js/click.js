openerp.fal_easy_reporting = function (instance) {
    var QWeb = instance.web.qweb,
        _lt = instance.web._lt,
        _t = instance.web._t;
    
    instance.web.FormView.include({
        on_click_export_data: function() {
            var self = this;
            var exported_fields = this.$el.find('div.fal_temp :first-child').val();
            var domains = instance.web.pyeval.eval('domain', this.$el.find('div.fal_temp_domain :first-child').val());
            var format_file = this.$el.find('span.fal_file_format :first-child').val();            
            if (!domains) {
                domains = []
            }
            if (!exported_fields) {
                alert(_t("Please select fields to export..."));
                return;
            }
            if (!format_file) {
                alert(_t("Please select format file to export..."));
                return;
            }
            exported_fields = $.map( exported_fields.split(','), function( val, i ) {
                return {name: val ,
                        label: val};
            });
            var model_fields = this.$el.find('span.fal_resource :first-child').val()
            exported_fields.unshift({name: 'id', label: 'External ID'});
            var export_format = 'xls';
            if(format_file == "\"CSV\""){
                export_format = "csv";
            }
            var ids_to_export = false;  /*this.$('#export_selection_only').prop('checked')
                    ? this.getParent().get_selected_ids()
                    : this.dataset.ids;
            */
            instance.web.blockUI();
            this.session.get_file({
                url: '/web/export/' + export_format,
                data: {data: JSON.stringify({
                    model: model_fields,
                    fields: exported_fields,
                    ids: ids_to_export,
                    domain: domains, //this.dataset.domain,
                    import_compat: 'yes',
                })},
                complete: instance.web.unblockUI,
            });
        },
        do_show: function(options) {
            var self = this;
            self._super(options);
            if(self.model == 'easy.exporting.wizard') {
                self.$buttons.append("<button id='easy_export' class='oe_highlight'>Export</button>")
                self.$buttons.find('button#easy_export').click(function(){
                    self.on_click_export_data();
                });
            }
        },
    });
}