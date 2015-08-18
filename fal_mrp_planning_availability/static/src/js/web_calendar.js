openerp.fal_mrp_planning_availability = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt,
        QWeb = instance.web.qweb;

    /**
     * Quick add view.
     *
     * Triggers a single event "added" with a single parameter "name", which is the
     * name entered by the user
     *
     * @class
     * @type {*}
     */
    instance.web_calendar.FalMrpQuickAdd = instance.web.Widget.extend({
        template: 'CalendarView.fal_mrp_quick_add',
        
        init: function(parent, dataset, buttons, options, data_template) {
            this._super(parent);
            this.dataset = dataset;
            this._buttons = buttons || false;
            this.options = options;

            // Can hold data pre-set from where you clicked on agenda
            this.data_template = data_template || {};
        },
        get_title: function () {
            var parent = this.getParent();
            if (_.isUndefined(parent)) {
                return _t("Add");
            }
            var title = 'Manufacture Order'
            return _t("Add: ") + title;
        },
        start: function () {
            var self = this;

            if (this.options.disable_quick_create) {
                this.$el.hide();
                this.slow_create();
                return;
            }
            
            var submit = this.$el.find(".oe_calendar_fal_mrp_quick_create_add");
            submit.click(function clickHandler() {
                submit.off('click', clickHandler);
                if (!self.quick_add()){
                   submit.on('click', clickHandler);                }
                self.focus();
            });
            this.$el.find(".oe_calendar_quick_create_close").click(function (ev) {
                ev.preventDefault();
                self.trigger('close');
            });
            self.$el.dialog({ title: this.get_title()});
            self.on('added', self, function() {
                self.trigger('close');
            });
            
            self.$el.on('dialogclose', self, function() {
                self.trigger('close');
            });
            
            self.dfm = new instance.web.form.DefaultFieldManager(self);
            self.dfm.extend_field_desc({
                production_ids: {
                    relation: "mrp.production",
                },
            });
            self.mrpMany2Many = new instance.web.form.FieldMany2Many(self.dfm, {
                attrs: {
                    class: 'oe_add_many2many_fal_mrp_production',
                    name: "production_ids",
                    string: _t("Manufacture Order"),
                    type: "many2many",
                    options: '{"no_open": True, "no_create": True}',
                    domain: [
                        ['state', 'not in', ['cancel', 'draft', 'done']],
                        ['fal_floating_production_date', '=', false],
                    ],
                },
            }); 
            self.mrpMany2Many.insertAfter(self.$el.find('label'));
        },
        focus: function() {
            this.$el.find('oe_add_many2many_fal_mrp_production').focus();
        },

        /**
         * Gathers data from the quick create dialog a launch quick_create(data) method
         */
        quick_add: function() {       
            if (this.mrpMany2Many.get_value()) {
                mrp_order_added_ids = this.mrpMany2Many.get_value()[0][2];
                return this.quick_create(mrp_order_added_ids) //.always(function() { return true; });
            }else{
                self.trigger('close');
            }            
        },
        
        /**
         * Handles saving data coming from quick create box
         */
        quick_create: function(data, options) {
            var self = this;
            var MrpProduction = new openerp.Model('mrp.production');
            var vals = {'fal_floating_production_date': this.data_template.fal_floating_production_date};
            MrpProduction.call('write',[data, vals])
                .then(function(){
                    jQuery.each(data, function(index, value) {
                        self.trigger('faladded', value);
                    });
                    self.trigger('close');
            });            
        },

        /**
         * Show full form popup
         */
         get_form_popup_infos: function() {
            var parent = this.getParent();
            var infos = {
                view_id: false,
                title: this.name,
            };
            if (!_.isUndefined(parent) && !(_.isUndefined(parent.ViewManager))) {
                infos.view_id = parent.ViewManager.get_view_id('form');
            }
            return infos;
        },
        slow_create: function(data) {
            //if all day, we could reset time to display 00:00:00
            
            var self = this;
            var def = $.Deferred();
            var defaults = {};
            var created = false;

            _.each($.extend({}, this.data_template, data), function(val, field_name) {
                defaults['default_' + field_name] = val;
            });
                        
            var pop_infos = self.get_form_popup_infos();
            var pop = new instance.web.form.FormOpenPopup(this);
            var context = new instance.web.CompoundContext(this.dataset.context, defaults);
            pop.show_element(this.dataset.model, null, this.dataset.get_context(defaults), {
                title: this.get_title(),
                disable_multiple_selection: true,
                view_id: pop_infos.view_id,
                // Ensuring we use ``self.dataset`` and DO NOT create a new one.
                create_function: function(data, options) {
                    return self.dataset.create(data, options).done(function(r) {
                    }).fail(function (r, event) {
                       if (!r.data.message) { //else manage by openerp
                            throw new Error(r);
                       }
                    });
                },
                read_function: function(id, fields, options) {
                    return self.dataset.read_ids.apply(self.dataset, arguments).done(function() {
                    }).fail(function (r, event) {
                        if (!r.data.message) { //else manage by openerp
                            throw new Error(r);
                        }
                    });
                },
            });
            pop.on('closed', self, function() {
                // ``self.trigger('close')`` would itself destroy all child element including
                // the slow create popup, which would then re-trigger recursively the 'closed' signal.  
                // Thus, here, we use a deferred and its state to cut the endless recurrence.
                if (def.state() === "pending") {
                    def.resolve();
                }
            });
            pop.on('create_completed', self, function(id) {
                created = true;
                self.trigger('slowadded');
            });
            def.then(function() {
                if (created) {
                    var parent = self.getParent();
                    parent.$calendar.fullCalendar('refetchEvents');
                }
                self.trigger('close');
            });
            return def;
        },
    });
    
    function get_fc_defaultOptions() {
        shortTimeformat = Date.CultureInfo.formatPatterns.shortTime;
        var dateFormat = Date.normalizeFormat(instance.web.strip_raw_chars(_t.database.parameters.date_format));
        return {
            weekNumberTitle: _t("W"),
            allDayText: _t("All day"),
            buttonText : {
                today:    _t("Today"),
                month:    _t("Month"),
                week:     _t("Week"),
                day:      _t("Day")
            },
            monthNames: Date.CultureInfo.monthNames,
            monthNamesShort: Date.CultureInfo.abbreviatedMonthNames,
            dayNames: Date.CultureInfo.dayNames,
            dayNamesShort: Date.CultureInfo.abbreviatedDayNames,
            firstDay: Date.CultureInfo.firstDayOfWeek,
            weekNumbers: true,
            axisFormat : shortTimeformat.replace(/:mm/,'(:mm)'),
            timeFormat : {
               // for agendaWeek and agendaDay               
               agenda: shortTimeformat + '{ - ' + shortTimeformat + '}', // 5:00 - 6:30
                // for all other views
                '': shortTimeformat.replace(/:mm/,'(:mm)')  // 7pm
            },
            titleFormat: {
                month: 'MMMM yyyy',
                week: dateFormat + "{ '&#8212;'"+ dateFormat,
                day: dateFormat,
            },
            columnFormat: {
                month: 'ddd',
                week: 'ddd ' + dateFormat,
                day: 'dddd ' + dateFormat,
            },
            weekMode : 'liquid',
            aspectRatio: 1.8,
            snapMinutes: 15,
        };
    }

    function isNullOrUndef(value) {
        return _.isUndefined(value) || _.isNull(value);
    }    

    function get_class(name) {
        return new instance.web.Registry({'tmp' : name}).get_object("tmp");
    }
    
    instance.web_calendar.CalendarView.include({        
        fal_mrp_quick_add_instance: 'instance.web_calendar.FalMrpQuickAdd',
        open_quick_create: function(data_template) {
            if(this.name != 'mrp.production.calendar'){
                return this._super.apply(this, arguments);
            }
            else{ 
                if (!isNullOrUndef(this.quick)) {
                    return this.quick.trigger('close');
                }
                var QuickCreate = get_class(this.fal_mrp_quick_add_instance);

                this.options.disable_quick_create =  this.options.disable_quick_create || !this.quick_add_pop;

                this.quick = new QuickCreate(this, this.dataset, true, this.options, data_template);
                this.quick.on('added', this, this.quick_created)
                        .on('slowadded', this, this.slow_created)
                        .on('faladded', this, this.refresh_event)
                        .on('close', this, function() {
                            this.quick.destroy();
                            delete this.quick;
                            this.$calendar.fullCalendar('unselect');
                        });
                this.quick.replace(this.$el.find('.oe_calendar_qc_placeholder'));
                this.quick.focus();
            }            
        },
        init_calendar: function () {
            res = this._super.apply(this, arguments);
            if(this.name == 'mrp.production.calendar'){            
                if (!this.topSidebar && this.options.$sidebar) {
                    this.topSidebar = new instance.web.Sidebar(this);
                    console.log(this.options.$sidebar);
                    this.topSidebar.appendTo(this.options.$sidebar);
                    this.topSidebar.add_items('other', _.compact([
                        { label: _t("Export"), callback: this.on_sidebar_export },
                    ]));
                    this.topSidebar.add_toolbar(this.fields_view.toolbar);
                    this.topSidebar.$el.hide();
                    
                    //this.options.$sidebar.add_toolbar(this.fields_view.toolbar);
                }                
            }
            return res
        },
        view_loading: function (fv) {
            res = this._super.apply(this, arguments);
            return res
        },
        do_button_action: function (name, id, callback) {
            this.handle_button(name, id, callback);
        },
        /**
         * Base handling of buttons, can be called when overriding do_button_action
         * in order to bypass parent overrides.
         *
         * The callback will be provided with the ``id`` as its parameter, in case
         * handle_button's caller had to alter the ``id`` (or even create one)
         * while not being ``callback``'s creator.
         *
         * This method should not be overridden.
         *
         * @param {String} name action name
         * @param {Object} id id of the record the action should be called on
         * @param {Function} callback should be called after the action is executed, if non-null
         */
        handle_button: function (name, id, callback) {
            var action = _.detect(this.columns, function (field) {
                return field.name === name;
            });
            if (!action) { return; }
            if ('confirm' in action && !window.confirm(action.confirm)) {
                return;
            }

            var c = new instance.web.CompoundContext();
            c.set_eval_context(_.extend({
                active_id: id,
                active_ids: [id],
                active_model: this.dataset.model
            }, this.records.get(id).toContext()));
            if (action.context) {
                c.add(action.context);
            }
            action.context = c;
            this.do_execute_action(
                action, this.dataset, id, _.bind(callback, null, id));
        },
        /**
         * Handles the activation of a record (clicking on it)
         *
         * @param {Number} index index of the record in the dataset
         * @param {Object} id identifier of the activated record
         * @param {instance.web.DataSet} dataset dataset in which the record is available (may not be the listview's dataset in case of nested groups)
         */
        do_activate_record: function (index, id, dataset, view) {
            this.dataset.ids = dataset.ids;
            this.select_record(index, view);
        },
        get_active_domain: function () {
            var self = this;
            return $.Deferred().resolve();
        },
        get_selection: function () {
            var result = {ids: [], records: []};
            //console.log(this);
            console.log($('.oe_calendar_record_selector:checked'));
            $('.oe_calendar_record_selector:checked').each(function(child){
                console.log($(this)[0].id);
                result.ids.push(parseInt($(this)[0].id));
                //records.push.apply(records, selection.records);
            });
            return result
        },
        get_selected_ids: function() {
            var ids = this.get_selection().ids;
            console.log('calendar', ids);
            return ids;
        },
        do_select: function (ids, records, deselected) {
            // uncheck header hook if at least one row has been deselected
            if (deselected) {
                this.$('.oe_calendar_record_selector').prop('checked', false);
            }

            if (!ids.length) {
                this.dataset.index = 0;
                if (this.topSidebar) {
                    this.topSidebar.$el.hide();
                }
                //this.compute_aggregates();
                return;
            }

            this.dataset.index = _(this.dataset.ids).indexOf(ids[0]);
            if (this.topSidebar) {
                this.options.$sidebar.show();
                this.topSidebar.$el.show();
            }
            /*
            this.compute_aggregates(_(records).map(function (record) {
                return {count: 1, values: record};
            }));
            */
        },
        do_hide: function () {
            if (this.topSidebar) {
                this.topSidebar.$el.hide();
            }
            this._super();
        },
        get_fc_init_options: function () {
            if(this.name != 'mrp.production.calendar'){
                return this._super.apply(this, arguments);
            }
            else{                
                var self = this;
                return  $.extend({}, get_fc_defaultOptions(), {
                    defaultView: (this.mode == "month")?"month":
                        (this.mode == "week"?"agendaWeek":
                         (this.mode == "day"?"agendaDay":"month")),
                    header: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'month,agendaWeek,agendaDay'
                    },
                    selectable: !this.options.read_only_mode && this.create_right,
                    selectHelper: true,
                    editable: !this.options.read_only_mode,
                    droppable: true,

                    // callbacks

                    eventDrop: function (event, _day_delta, _minute_delta, _all_day, _revertFunc) {
                        var data = self.get_event_data(event);
                        self.proxy('update_record')(event._id, data); // we don't revert the event, but update it.
                        /*
                        var data = self.get_event_data(event);
                        $('<div></div>').appendTo('body')
                                            .html('<div><h6>Which date that you want to change??</h6></div>')
                                            .dialog({
                                                modal: true, title: 'Confirmation', zIndex: 10000, autoOpen: true,
                                                width: 'auto', resizable: false,
                                                buttons: {
                                                    'Schedule Date': function () {
                                                        self.proxy('update_record')(event._id, data); // we don't revert the event, but update it.
                                                        $(this).dialog("close");
                                                    },
                                                    'Fixed Production Date': function () {
                                                        data['fal_fixed_production_date'] = data.date_planned;
                                                        delete data.date_planned;
                                                        self.proxy('update_record')(event._id, data); // we don't revert the event, but update it.
                                                        $(this).dialog("close");
                                                    }
                                                },
                                                close: function (event, ui) {
                                                    _revertFunc()
                                                    $(this).remove();
                                                }
                                            });
                        */
                    },
                    eventResize: function (event, _day_delta, _minute_delta, _revertFunc) {
                        var data = self.get_event_data(event);
                        self.proxy('update_record')(event._id, data);
                    },
                    eventRender: function (event, element, view) {
                        var MrpProduction = new openerp.Model('mrp.production');
                        /*MrpProduction.query(['fal_fixed_production_date']).filter([['id','=',event._id]]).first().then(function(production_id) {
                            if(production_id.fal_fixed_production_date){
                                element.find('.fc-event-title').html('<input type="checkbox" class="oe_calendar_record_selector" id="'+ event._id +'"/> ' + event.title + ' <input type="radio" class="oe_calendar_radio_is_fixed" checked/>');
                            }else{
                                element.find('.fc-event-title').html('<input type="checkbox" class="oe_calendar_record_selector" id="'+ event._id +'"/> ' + event.title);
                            }
                        });*/
                        element.find('.fc-event-title').html('<input type="checkbox" class="oe_calendar_record_selector" id="'+ event._id +'"/> ' + event.title);
                    },
                    
                    eventAfterRender: function (event, element, view) {
                        if ((view.name !== 'month') && (((event.end-event.start)/60000)<=30)) {
                            //if duration is too small, we see the html code of img
                            var current_title = $(element.find('.fc-event-time')).text();
                            var new_title = current_title.substr(0,current_title.indexOf("<img")>0?current_title.indexOf("<img"):current_title.length);
                            element.find('.fc-event-time').html(new_title);
                        }
                        //console.log($('.oe_calendar_record_selector'));
                        $('.oe_calendar_record_selector').click(
                            function(e) {
                                e.stopPropagation();
                                selection = self.get_selection();
                                self.do_select(selection.ids, selection.records, false);
                            }
                        );
                    },
                    eventClick: function (event) { 
                        if($('.oe_calendar_record_selector:checked').length > 0){
                            return true;
                        }else{
                            self.open_event(event._id,event.title);
                        }
                    },
                    select: function (start_date, end_date, all_day, _js_event, _view) {
                        var data_template = self.get_event_data({
                            start: start_date,
                            end: end_date,
                            allDay: all_day,
                        });
                        self.open_quick_create(data_template);

                    },

                    unselectAuto: false,
                });

            }
        }
    });
};