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

class procurement_order(orm.Model):
    _inherit = 'procurement.order'

    def _procure_confirm(self, cr, uid, ids=None, use_new_cursor=False, context=None):
        '''
        Call the scheduler to check the procurement order

        @param self: The object pointer
        @param cr: The current row, from the database cursor,
        @param uid: The current user ID for security checks
        @param ids: List of selected IDs
        @param use_new_cursor: False or the dbname
        @param context: A standard dictionary for contextual values
        @return:  Dictionary of values
        '''
        if context is None:
            context = {}
        try:
            if use_new_cursor:
                cr = pooler.get_db(use_new_cursor).cursor()
            wf_service = netsvc.LocalService("workflow")

            procurement_obj = self.pool.get('procurement.order')
            if not ids:
                ids = procurement_obj.search(cr, uid, [('state', '=', 'exception')], order="date_planned")
            for id in ids:
                wf_service.trg_validate(uid, 'procurement.order', id, 'button_restart', cr)
            if use_new_cursor:
                cr.commit()
            company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id
            maxdate = (datetime.today() + relativedelta(days=company.schedule_range)).strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
            start_date = fields.datetime.now()
            offset = 0
            report = []
            report_total = 0
            report_except = 0
            report_later = 0
            while True:
                ids = procurement_obj.search(cr, uid, [('state', '=', 'confirmed'), ('procure_method', '=', 'make_to_order')], offset=offset, limit=500, order='priority, date_planned', context=context)
                for proc in procurement_obj.browse(cr, uid, ids, context=context):
                    if maxdate >= proc.date_planned:
                        wf_service.trg_validate(uid, 'procurement.order', proc.id, 'button_check', cr)
                    else:
                        offset += 1
                        report_later += 1

                    if proc.state == 'exception':
                        report.append(_('PROC %d: on order - %3.2f %-5s - %s') % \
                                (proc.id, proc.product_qty, proc.product_uom.name,
                                    proc.product_id.name))
                        report_except += 1
                    report_total += 1
                if use_new_cursor:
                    cr.commit()
                if not ids:
                    break
            offset = 0
            ids = []
            while True:
                report_ids = []
                ids = procurement_obj.search(cr, uid, [('state', '=', 'confirmed'), ('procure_method', '=', 'make_to_stock')], offset=offset)
                for proc in procurement_obj.browse(cr, uid, ids):
                    if maxdate >= proc.date_planned:
                        wf_service.trg_validate(uid, 'procurement.order', proc.id, 'button_check', cr)
                        report_ids.append(proc.id)
                    else:
                        report_later += 1
                    report_total += 1

                    if proc.state == 'exception':
                        report.append(_('PROC %d: from stock - %3.2f %-5s - %s') % \
                                (proc.id, proc.product_qty, proc.product_uom.name,
                                    proc.product_id.name,))
                        report_except += 1


                if use_new_cursor:
                    cr.commit()
                offset += len(ids)
                if not ids: break
            end_date = fields.datetime.now()
            if uid:
                request = self.pool.get('res.request')
                summary = '''Here is the procurement scheduling report.

        Start Time: %s
        End Time: %s
        Total Procurements processed: %d
        Procurements with exceptions: %d
        Skipped Procurements (scheduled date outside of scheduler range) %d

        Exceptions:\n'''% (start_date, end_date, report_total, report_except, report_later)
                summary += '\n'.join(report)
                request.create(cr, uid,
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
        return {}
        
#end of procurement_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
