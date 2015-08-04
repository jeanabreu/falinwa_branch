openerp.fal_mrp_planning_availability = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt,
        QWeb = instance.web.qweb;

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
    
    instance.web_calendar.CalendarView.include({        
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
                    },
                    eventResize: function (event, _day_delta, _minute_delta, _revertFunc) {
                        var data = self.get_event_data(event);
                        self.proxy('update_record')(event._id, data);
                    },
                    eventRender: function (event, element, view) {
                        element.find('.fc-event-title').html(event.title);
                    },
                    eventAfterRender: function (event, element, view) {
                        if ((view.name !== 'month') && (((event.end-event.start)/60000)<=30)) {
                            //if duration is too small, we see the html code of img
                            var current_title = $(element.find('.fc-event-time')).text();
                            var new_title = current_title.substr(0,current_title.indexOf("<img")>0?current_title.indexOf("<img"):current_title.length);
                            element.find('.fc-event-time').html(new_title);
                        }
                    },
                    eventClick: function (event) { self.open_event(event._id,event.title); },
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