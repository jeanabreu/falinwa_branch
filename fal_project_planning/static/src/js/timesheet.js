
openerp.fal_project_planning = function(instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

    instance.fal_project_planning.BudgetTimesheet = instance.web.form.FormWidget.extend(instance.web.form.ReinitializeWidgetMixin, {
        events: {
            "click .oe_timesheet_budget_task a": "go_to",
        },
        ignore_fields: function() {
            return ['line_id'];
        },
        init: function() {
            this._super.apply(this, arguments);
            var self = this;
            this.set({
                sheets: [],
                date: false,
                date_start: false,
            });
            this.updating = false;
            this.defs = [];
            this.field_manager.on("field_changed:fal_project_timesheet_budget_line_ids", this, this.query_sheets);
            this.field_manager.on("field_changed:date_start", this, function() {
                this.set({"date_start": instance.web.str_to_date(this.field_manager.get_field_value("date_start"))});
            });
            this.field_manager.on("field_changed:date", this, function() {
                this.set({"date": instance.web.str_to_date(this.field_manager.get_field_value("date"))});
            });
            this.field_manager.on("field_changed:user_id", this, function() {
                this.set({"user_id": this.field_manager.get_field_value("user_id")});
            });
            this.on("change:sheets", this, this.update_sheets);
            this.res_o2m_drop = new instance.web.DropMisordered();
            this.render_drop = new instance.web.DropMisordered();
            this.description_line = _t("/");
            // Original save function is overwritten in order to wait all running deferreds to be done before actually applying the save.
            this.view.original_save = _.bind(this.view.save, this.view);
            this.view.save = function(prepend_on_create){
                self.prepend_on_create = prepend_on_create;
                return $.when.apply($, self.defs).then(function(){
                    return self.view.original_save(self.prepend_on_create);
                });
            };
        },
        go_to: function(event) {
            var id = JSON.parse($(event.target).data("id"));
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: "project.task",
                res_id: id,
                views: [[false, 'form']],
                target: 'current'
            });
        },
        query_sheets: function() {
            var self = this;
            if (self.updating)
                return;
            var commands = this.field_manager.get_field_value("fal_project_timesheet_budget_line_ids");
            this.res_o2m_drop.add(new instance.web.Model(this.view.model).call("resolve_2many_commands", ["fal_project_timesheet_budget_line_ids", commands, [], 
                    new instance.web.CompoundContext()]))
                .done(function(result) {
                self.querying = true;
                self.set({sheets: result});
                self.querying = false;
            });
        },
        update_sheets: function() {
            var self = this;
            if (self.querying)
                return;
            self.updating = true;
            self.field_manager.set_values({fal_project_timesheet_budget_line_ids: self.get("sheets")}).done(function() {
                self.updating = false;
            });
        },
        initialize_field: function() {
            instance.web.form.ReinitializeWidgetMixin.initialize_field.call(this);
            var self = this;
            self.on("change:sheets", self, self.initialize_content);
            self.on("change:date", self, self.initialize_content);
            self.on("change:date_start", self, self.initialize_content);
            self.on("change:user_id", self, self.initialize_content);
        },
        initialize_content: function() {
            var self = this;
            if (self.setting)
                return;
            // don't render anything until we have date_to and date_from
            if (!self.get("date") || !self.get("date_start"))
                return;
            this.destroy_content();

            // it's important to use those vars to avoid race conditions
            var dates;
            var tasks;
            var task_names;
            var default_get;
            return this.render_drop.add(new instance.web.Model("fal.project.timesheet.budget.line").call("default_get", [
                ['task_id','date','name','user_id','unit_amount','project_id'],
                new instance.web.CompoundContext({'user_id': self.get('user_id')})]).then(function(result) {
                default_get = result;
                // calculating dates
                dates = [];
                var start = self.get("date_start");
                var end = self.get("date");
                while (start <= end) {
                    dates.push(start);
                    start = start.clone().addDays(1);
                }
                // group by task
                tasks = _(self.get("sheets")).chain()
                .map(function(el) {
                    // much simpler to use only the id in all cases
                    if (typeof(el.task_id) === "object")
                        el.task_id = el.task_id[0];
                    return el;
                })
                .groupBy("task_id").value();
                var task_ids = _.map(_.keys(tasks), function(el) { return el === "false" ? false : Number(el) });

                return new instance.web.Model("fal.project.timesheet.budget.line").call("multi_on_change_task_id", [[], task_ids,
                    new instance.web.CompoundContext({'user_id': self.get('user_id')})]).then(function(tasks_defaults) {
                    tasks = _(tasks).chain().map(function(lines, task_id) {
                        task_defaults = _.extend({}, default_get, (tasks_defaults[task_id] || {}).value || {});
                        // group by days
                        task_id = task_id === "false" ? false :  Number(task_id);
                        var index = _.groupBy(lines, "date");
                        var days = _.map(dates, function(date) {
                            var day = {day: date, lines: index[instance.web.date_to_str(date)] || []};
                            // add line where we will insert/remove hours
                            var to_add = _.find(day.lines, function(line) { return line.name === self.description_line });
                            if (to_add) {
                                day.lines = _.without(day.lines, to_add);
                                day.lines.unshift(to_add);
                            } else {
                                day.lines.unshift(_.extend(_.clone(task_defaults), {
                                    name: self.description_line,
                                    unit_amount: 0,
                                    date: instance.web.date_to_str(date),
                                    task_id: task_id,
                                    project_id: self.field_manager.datarecord.id,
                                }));
                            }
                            return day;
                        });
                        return {task: task_id, days: days, task_defaults: task_defaults};
                    }).value();

                    // we need the name_get of the tasks
                    return new instance.web.Model("project.task").call("name_get", [_.pluck(tasks, "task"),
                        new instance.web.CompoundContext()]).then(function(result) {
                        task_names = {};
                        _.each(result, function(el) {
                            task_names[el[0]] = el[1];
                        });
                        tasks = _.sortBy(tasks, function(el) {
                            return task_names[el.task];
                        });
                    });;
                });
            })).then(function(result) {
                // we put all the gathered data in self, then we render
                self.dates = dates;
                self.tasks = tasks;
                self.task_names = task_names;
                self.default_get = default_get;
                //real rendering
                self.display_data();
            });
        },
        destroy_content: function() {
            if (this.dfm) {
                this.dfm.destroy();
                this.dfm = undefined;
            }
        },
        is_valid_value:function(value){
            var split_value = value.split(":");
            var valid_value = true;
            if (split_value.length > 2)
                return false;
            _.detect(split_value,function(num){
                if(isNaN(num)){
                    valid_value = false;
                }
            });
            return valid_value;
        },
        display_data: function() {
            var self = this;
            self.$el.html(QWeb.render("fal_project_planning.BudgetTimesheet", {widget: self}));
            _.each(self.tasks, function(task) {
                _.each(_.range(task.days.length), function(day_count) {
                    if (!self.get('effective_readonly')) {
                        self.get_box(task, day_count).val(self.sum_box(task, day_count, true)).change(function() {
                            var num = $(this).val();
                            if (self.is_valid_value(num)){
                                num = (num == 0)?0:Number(self.parse_client(num));
                            }
                            if (isNaN(num)) {
                                $(this).val(self.sum_box(task, day_count, true));
                            } else {
                                task.days[day_count].lines[0].unit_amount += num - self.sum_box(task, day_count);
                                //var product = (task.days[day_count].lines[0].product_id instanceof Array) ? task.days[day_count].lines[0].product_id[0] : task.days[day_count].lines[0].product_id
                                //var journal = (task.days[day_count].lines[0].journal_id instanceof Array) ? task.days[day_count].lines[0].journal_id[0] : task.days[day_count].lines[0].journal_id
                                self.defs.push(new instance.web.Model("fal.project.timesheet.budget.line").call("on_change_unit_amount", [[], task.days[day_count].lines[0].unit_amount, false, false, false]).then(function(res) {
                                    //task.days[day_count].lines[0]['amount'] = res.value.amount || 0;
                                    self.display_totals();
                                    self.sync();
                                }));
                                if(!isNaN($(this).val())){
                                    $(this).val(self.sum_box(task, day_count, true));
                                }
                            }
                        });
                    } else {
                        self.get_box(task, day_count).html(self.sum_box(task, day_count, true));
                    }
                });
            });
            self.display_totals();
            self.$(".oe_timesheet_budget_adding button").click(_.bind(this.init_add_task, this));
        },
        init_add_task: function() {
            var self = this;
            if (self.dfm)
                return;
            self.$(".oe_timesheet_budget_add_row").show();
            self.dfm = new instance.web.form.DefaultFieldManager(self);
            self.dfm.extend_field_desc({
                task: {
                    relation: "project.task",
                },
            });
            self.task_m2o = new instance.web.form.FieldMany2One(self.dfm, {
                attrs: {
                    name: "task",
                    type: "many2one",
                    domain: [
                        ['project_id', '=', self.field_manager.datarecord.id],
                        ['id', 'not in', _.pluck(self.tasks, "task")],
                    ],/*
                    context: {
                        default_use_timesheets: 1,
                        default_type: "contract",
                    },*/
                    modifiers: '{"required": true}',
                },
            });
            self.task_m2o.prependTo(self.$(".oe_timesheet_budget_add_row td"));
            /*
            self.userdfm = new instance.web.form.DefaultFieldManager(self);
            self.userdfm.extend_field_desc({
                user: {
                    relation: "res.users",
                },
            });
            
            self.user_m2o = new instance.web.form.FieldMany2One(self.userdfm, {
                attrs: {
                    name: "user",
                    type: "many2one",
                    modifiers: '{"required": true}',
                },
            });
            self.user_m2o.prependTo(self.$(".oe_timesheet_budget_add_row td"));
            */
            self.$(".oe_timesheet_budget_add_row button").click(function() {
                var id = self.task_m2o.get_value();
                if (id === false) {
                    self.dfm.set({display_invalid_fields: true});
                    return;
                }
                var ops = self.generate_o2m_value();
                new instance.web.Model("fal.project.timesheet.budget.line").call("multi_on_change_task_id", [[], [id],
                    new instance.web.CompoundContext({'user_id': self.get('user_id')})]).then(function(res) {
                    res = res[id];
                    var def = _.extend({}, self.default_get, res.value, {
                        name: self.description_line,
                        unit_amount: 0,
                        date: instance.web.date_to_str(self.dates[0]),
                        task_id: id,
                        project_id: self.field_manager.datarecord.id,
                    });
                    ops.push(def);
                    self.set({"sheets": ops});
                });
            });
        },
        get_box: function(task, day_count) {
            return this.$('[data-task="' + task.task + '"][data-day-count="' + day_count + '"]');
        },
        get_total: function(task) {
            return this.$('[data-task-total="' + task.task + '"]');
        },
        get_day_total: function(day_count) {
            return this.$('[data-day-total="' + day_count + '"]');
        },
        get_super_total: function() {
            return this.$('.oe_timesheet_budget_supertotal');
        },
        sum_box: function(task, day_count, show_value_in_hour) {
            var line_total = 0;
            _.each(task.days[day_count].lines, function(line) {
                line_total += line.unit_amount;
            });
            return (show_value_in_hour && line_total != 0)?this.format_client(line_total):line_total;
        },
        display_totals: function() {
            var self = this;
            var day_tots = _.map(_.range(self.dates.length), function() { return 0 });
            var super_tot = 0;
            _.each(self.taskss, function(task) {
                var acc_tot = 0;
                _.each(_.range(self.dates.length), function(day_count) {
                    var sum = self.sum_box(task, day_count);
                    acc_tot += sum;
                    day_tots[day_count] += sum;
                    super_tot += sum;
                });
                self.get_total(task).html(self.format_client(acc_tot));
            });
            _.each(_.range(self.dates.length), function(day_count) {
                self.get_day_total(day_count).html(self.format_client(day_tots[day_count]));
            });
            self.get_super_total().html(self.format_client(super_tot));
        },
        sync: function() {
            var self = this;
            self.setting = true;
            self.set({sheets: this.generate_o2m_value()});
            self.setting = false;
        },
        //converts hour value to float
        parse_client: function(value) {
            return instance.web.parse_value(value, { type:"float_time" });
        },
        //converts float value to hour
        format_client:function(value){
            return instance.web.format_value(value, { type:"float_time" });
        },
        generate_o2m_value: function() {
            var self = this;
            var ops = [];
            var ignored_fields = self.ignore_fields();
            _.each(self.tasks, function(task) {
                _.each(task.days, function(day) {
                    _.each(day.lines, function(line) {
                        if (line.unit_amount !== 0) {
                            var tmp = _.clone(line);
                            tmp.id = undefined;
                            _.each(line, function(v, k) {
                                if (v instanceof Array) {
                                    tmp[k] = v[0];
                                }
                            });
                            // we remove line_id as the reference to the _inherits field will no longer exists
                            tmp = _.omit(tmp, ignored_fields);
                            ops.push(tmp);
                        }
                    });
                });
            });
            return ops;
        },
    });

    instance.web.form.custom_widgets.add('budget_timesheet', 'instance.fal_project_planning.BudgetTimesheet');

};
