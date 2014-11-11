# -*- coding: utf-8 -*-

import base64
from cStringIO import StringIO
import csv
from openerp.osv import fields, orm
from openerp.tools.translate import _

class easy_exporting_wizard(orm.TransientModel):
    _name = "easy.exporting.wizard"
    _description = "Easy Exporting Wizard"
    
    _columns = {
        'model_id': fields.many2one('ir.model', 'Object', required=True, ondelete='cascade', help="Select the object on which want to be download."),
        'resource': fields.char('Resource', size=128),
        'template_id' : fields.many2one('ir.exports', 'Template', required=True, help="Select the template on which want to be download."),
        'filter_ids' : fields.many2many('ir.filters', 'easy_export_filter_rel', 'easy_export_id', 'filter_id', 'Filter', help="Select the filter on which want to be download."),
        'from_date': fields.date('From'),
        'to_date': fields.date('To'),
        'temp' : fields.text('temp'),
        'temp_domain' : fields.text('Domain'),
        'temp_file' : fields.binary('File'),
        'temp_file_name' : fields.char('name',size=64),
        'file_format' : fields.selection([('Excel','Excel'),('CSV','CSV')], 'File Format', required=True),
    }

    _defaults = {
        'file_format': 'Excel',
    }

    def onchange_model_id(self, cr, uid, ids, model_id, context=None):
        if context is None:
            context = {}
        res = {}
        model_obj = self.pool.get('ir.model')
        res['value'] = { 'resource' : False, 'template_id': False, 'temp':'', 'filter_ids': [], 'temp_filter_ids': ''}
        if model_id:
            model = model_obj.browse(cr, uid, model_id, context)
            res['value'] = { 'resource' : model.model, 'template_id': False, 'temp':'', 'filter_ids': [], 'temp_filter_ids': ''}
        return res
        
    def onchange_template_id(self, cr, uid, ids, template_id, context=None):
        if context is None:
            context = {}
        res = {}
        export_obj = self.pool.get('ir.exports')
        if template_id:
            export = export_obj.browse(cr, uid, template_id, context)
            temp_field = []
            for field in export.export_fields:
                temp_field.append(field.name)
            out = ','.join(temp_field)
            res['value'] = { 'temp':out}
        return res
        
    def onchange_filter_ids(self, cr, uid, ids, filter_ids, from_date, to_date, resource, context=None):
        if context is None:
            context = {}
        res = {}
        filter_obj = self.pool.get('ir.filters')
        res['value'] = { 'temp_domain': ''}
        out = ''
        temp_domain = []
        if filter_ids[0][2]:
            for filter in filter_obj.browse(cr, uid, filter_ids[0][2]):
                for dom in eval(filter.domain):
                    temp_domain.append(dom)
        if from_date and to_date:
            resource_obj = self.pool.get(resource)
            resource_fields = resource_obj.fields_get(cr, uid)
            if 'date' in resource_fields:
                temp_domain.append(['date','>=',from_date])
                temp_domain.append(['date','<=',to_date])            
            else:            
                temp_domain.append(['create_date','>=',from_date])
                temp_domain.append(['create_date','<=',to_date])  
        out += str(temp_domain)
        res['value'] = { 'temp_domain':out}
        return res
        
        
    """    
    def action_next(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0]        
        object_obj = self.pool.get(data_wizard.model_id.model)
        obj_ids = object_obj.search(cr, uid, [], context=context)
        temp_field = []
        for field in data_wizard.template_id.export_fields:
            temp_field.append(field.name)
        export = object_obj.read(cr, uid, obj_ids, temp_field, context=context)
        out=base64.encodestring(str(export))
        print export
        
        #modif start
        fp = StringIO()
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        writer.writerow([name.encode('utf-8') for name in temp_field])
        for data in export:
            row = []
            for l,d in data.items():
                if isinstance(d, basestring):
                    d = d.replace('\n',' ').replace('\t',' ')
                    try:
                        d = d.encode('utf-8')
                    except UnicodeError:
                        pass
                if d is False: d = None
                row.append(d)
            writer.writerow(row)
        fp.seek(0)
        data = fp.read()
        fp.close()
        print data
        self.write(cr, uid, ids, {'state': 'done', 'temp_file':data, 'temp_file_name': data_wizard.model_id.model + '.csv'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'easy.exporting.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
             }
    """    
#end of easy_exporting_wizard()