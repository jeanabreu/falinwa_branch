# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import netsvc
from openerp import pooler
from openerp.osv import orm
from openerp.osv import fields
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import tools

def _links_get(self, cr, uid, context=None):
    obj = self.pool.get('res.request.link')
    ids = obj.search(cr, uid, [], context=context)
    res = obj.read(cr, uid, ids, ['object', 'name'], context)
    return [(r['object'], r['name']) for r in res]
    
class res_request(orm.Model):
    _name = 'res.request'

    _columns = {
        'create_date': fields.datetime('Created Date', readonly=True),
        'name': fields.char('Subject', states={'waiting':[('readonly',True)],'active':[('readonly',True)],'closed':[('readonly',True)]}, required=True, size=128),
        'active': fields.boolean('Active'),
        'priority': fields.selection([('0','Low'),('1','Normal'),('2','High')], 'Priority', states={'waiting':[('readonly',True)],'closed':[('readonly',True)]}, required=True),
        'act_from': fields.many2one('res.users', 'From', required=True, readonly=True, states={'closed':[('readonly',True)]}, select=1),
        'act_to': fields.many2one('res.users', 'To', required=True, states={'waiting':[('readonly',True)],'closed':[('readonly',True)]}, select=1),
        'body': fields.text('Request', states={'waiting':[('readonly',True)],'closed':[('readonly',True)]}),
        'date_sent': fields.datetime('Date', readonly=True),
        'trigger_date': fields.datetime('Trigger Date', states={'waiting':[('readonly',True)],'closed':[('readonly',True)]}, select=1),
        'ref_partner_id':fields.many2one('res.partner', 'Partner Ref.', states={'closed':[('readonly',True)]}),
        'ref_doc1':fields.reference('Document Ref 1', selection=_links_get, size=128, states={'closed':[('readonly',True)]}),
        'ref_doc2':fields.reference('Document Ref 2', selection=_links_get, size=128, states={'closed':[('readonly',True)]}),
        'state': fields.selection([('draft','draft'),('waiting','waiting'),('active','active'),('closed','closed')], 'Status', required=True, readonly=True),
    }
    
    _defaults = {
        'act_from': lambda obj,cr,uid,context=None: uid,
        'state': 'draft',
        'active': True,
        'priority': '1',
    }
    _order = 'priority desc, trigger_date, create_date desc'
    _table = 'res_request'
#end of res_request()

class procurement_order(orm.Model):
    _inherit = 'procurement.order'
    
    def run_scheduler(self, cr, uid, use_new_cursor=False, company_id=False, context=None):
        res = super(procurement_order, self).run_scheduler(cr, uid, use_new_cursor=use_new_cursor, context=context)
        try:
            if use_new_cursor:
                cr = pooler.get_db(use_new_cursor).cursor()
            request = self.pool.get('res.request')
            summary = "Procurement run successfuly"
            request_id = request.create(cr, uid,
                {'name': "Procurement Processing Report.",
                    'act_from': uid,
                    'act_to': uid,
                    'body': summary,
                })
            if use_new_cursor:
                cr.commit()
        finally:
            if use_new_cursor:
                try:
                    cr.close()
                except Exception:
                    pass
        return res
                
#end of procurement_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
