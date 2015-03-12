# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from operator import itemgetter
from openerp.osv import fields, orm
import time
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.tools.translate import _
from openerp.tools import html2plaintext

class crm_lead(orm.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    def _get_delegates(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for opportunities in self.browse(cr,uid,ids,context=context):
            delegates = []
            for set in opportunities.package_ids:
                if set.delegated_id and set.delegated_id.name not in delegates:
                    delegates.append(set.delegated_id.name)            
            res[opportunities.id] = "; ".join(delegates)
        return res
        
    def _get_result(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for opportunities in self.browse(cr,uid,ids,context=context):
            i = 0.00
            if opportunities.expected_finished_date:
                efd = datetime.strptime(opportunities.expected_finished_date,'%Y-%m-%d').date()
                i = efd - date.today()
                i = i.days
            res[opportunities.id] = i
        return res
        
    _columns = {
        'package_ids' : fields.one2many('fal.sup.management.package','crm_lead_id','Set'),
        'rfq_date' : fields.date('RFQ Date'),
        'expected_finished_date' : fields.date('Expected Finished Date'),
        'delegates_to' : fields.function(_get_delegates, type='text', string='Delegates To', store=True),
        'efd_min_cd' : fields.function(_get_result, type="float", string="EFD Minus CD", store=False),
    }
    
    def _get_color_view(self, cr, uid, ids=False, context=None):
        if not ids:
            ids = self.search(cr, uid, [])
        return self.get_color_view(cr, uid, ids, context=context)
        
    def get_color_view(self, cr, uid, ids, context=None):
        res = {}
        for op in self.browse(cr, uid, ids, context=context):            
            #white:0, red:2, blue:7 , yellow:3
            color = 0
            if op.stage_id.name == 'RFQ Study':            
                if op.date_action:
                    da = datetime.strptime(op.date_action, '%Y-%m-%d').date()
                    if da <= date.today():
                        color = 2
                        
                if op.expected_finished_date:
                    efd = datetime.strptime(op.expected_finished_date, '%Y-%m-%d').date()
                    if efd - date.today() < timedelta(1):
                        color = 3
                    if efd - date.today() < timedelta(0):
                        color = 2
                                                 
                self.write(cr , uid, op.id, {'color': color})
        return True

    def _create_nextaction_reminder(self, cr, uid, ids=False, context=None):
        if not ids:
            ids = self.search(cr, uid, [('stage_id.name','=','RFQ Study')])
        return self.create_nextaction_reminder(cr, uid, ids, context=context)

    def create_nextaction_reminder(self, cr, uid, ids, context=None):
        mail_message_obj = self.pool.get('mail.message')
        for op in self.browse(cr, uid, ids):
            if op.date_action:
                da = datetime.strptime(op.date_action, '%Y-%m-%d').date()
                if da <= date.today():
                    temp = []
                    temp_partner = [op.user_id.partner_id.id]
                    #folowers = self._get_followers(cr, uid, [op.id], None, None, context=context)[po.id]['message_follower_ids']
                    message_id = self.message_post(cr, uid, [op.id], body="Next action date already exceeds on this opportunity, Please followup this opportunity", subtype='mt_comment', partner_ids= temp_partner, context=context)
                    mail_message_obj.write(cr, uid, [message_id], {'company_id':False})                    
        return True
        
#end of crm_lead()

class fal_sup_management_package(orm.Model):
    _name = "fal.sup.management.package"
    _description = "Set"
    _order = "rfq_date_rel desc"
    
    def _get_supplier(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for set in self.browse(cr,uid,ids,context=context):
            supplier_name = False
            for set_line in set.package_line_ids:
                if set_line.state == 'PO Launch':
                    supplier_name = set_line.supplier_name
            res[set.id] = supplier_name
        return res
    
    def _get_set_line(self, cr, uid, ids, context=None):
        result = {}
        for partner in self.pool.get('res.partner').browse(cr, uid, ids, context):
            for set in partner.pakckage_ids:
                result[set.id] = True
        return result.keys()
        
    _columns = {
        'crm_lead_id' : fields.many2one('crm.lead','CRM Lead'),
        'rfq_date_rel' : fields.related('crm_lead_id', 'rfq_date', type='date', string='RFQ Date', store=True, readonly=True),
        'expected_finished_date_rel' : fields.related('crm_lead_id', 'expected_finished_date', type='date', string='Expected Finished Date', readonly=True),
        'efd_min_cd_rel' : fields.related('crm_lead_id', 'efd_min_cd', type='float', string='EFD Minus CD', readonly=True),
        'name' : fields.char('Name', size=128, required=True),
        'description' : fields.text('Description'),
        'comment' : fields.text('Comment'),
        'package_line_ids' : fields.one2many('fal.sup.management.package.line', 'package_id', 'Packages Line'),
        'supplier_name' : fields.function(_get_supplier, type='text', string='Final Supplier', store=True),
        'delegated_id' : fields.many2one('res.users', 'Delegated to', track_visibility='onchange'),
        'salesperson_id' : fields.related('crm_lead_id','user_id', type='many2one', relation='res.users', string='Salesperson', readonly=True, store=True),
        'state' : fields.selection([('Pending','Pending'),('Progress','Progress'),('Finished','Finished')], 'State' , required=True),
    }

    _defaults = {
        'state' : 'Pending',
    }

    def write(self, cr, uid, ids, vals, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(fal_sup_management_package, self).write(cr, uid, ids, vals, context)
        op_obj = self.pool.get('crm.lead')
        stage_obj = self.pool.get('crm.case.stage')
        for set in self.browse(cr, uid, ids):
            temp = []
            for set_id in set.crm_lead_id.package_ids :
                if set_id.state != 'Finished':
                    temp.append(set_id.id)
            if not temp:
                stage_id = stage_obj.search(cr, uid, [('name','=','RFQ Answered')], limit=1, context=context)
                if stage_id:
                    op_obj.write(cr, uid, set.crm_lead_id.id, {'stage_id':stage_id[0]}, context)
                else:
                    raise osv.except_osv(_('Error!'), _('There is no RFQ Answered stage. Please configure the stage first.'))
        return res
            
#end of fal_sup_management_package()

class fal_sup_management_package_line(orm.Model):
    _name = "fal.sup.management.package.line"
    _description= "Set Line"
    
    _columns = {
        'supplier_name' : fields.text('Supplier', required=True),
        'description' : fields.text('Description'),
        'comment' : fields.text('Comment'),
        'package_id' : fields.many2one('fal.sup.management.package', 'Set', required=True),
        'state' : fields.selection([('PO Launch','PO Launch'), ('Inquired','Inquired'),('Inquiring','Inquiring'),('No data','No data'),('Cancel','Cancel')], 'Status'),
    }

#end of fal_sup_management_package_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
