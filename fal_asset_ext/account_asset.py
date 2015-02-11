# -*- encoding: utf-8 -*-

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class account_asset_category(orm.Model):
    _name = 'account.asset.category'
    _inherit = 'account.asset.category'

    _columns = {
        'simple_prorata' : fields.boolean('Simple Prorata')
    }
    
#end of account_asset_category()

class account_asset_asset(orm.Model):
    _name = 'account.asset.asset'
    _inherit = 'account.asset.asset'

    def _compute_board_amount(self, cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=None):
        res = super(account_asset_asset, self)._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date)            
        if asset.prorata and asset.simple_prorata:
            res = 0
            if i == undone_dotation_number:
                res = residual_amount
            else:
                if asset.method == 'linear':
                    res = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                elif asset.method == 'degressive':
                    res = residual_amount * asset.method_progress_factor
        return res

    def _get_asset_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.asset.depreciation.line').browse(cr, uid, ids, context=context):
            result[line.asset_id.id] = True
        return result.keys()

    def _fal_closing_date(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for asset in self.browse(cr, uid, ids, context=context):
            temp_last_date = False
            for depreciation in asset.depreciation_line_ids:
                if temp_last_date < depreciation.depreciation_date:
                    temp_last_date = depreciation.depreciation_date
            res[asset.id] = temp_last_date
        return res

    _columns = {
        'simple_prorata' : fields.boolean('Simple Prorata')
        'fal_closing_date' : fields.function(_fal_closing_date, string='Closing Date', type='date', 
            store={
                'account.asset.asset' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'account.asset.depreciation.line': (_get_asset_fal, None, 10),
            }, help="The Closing Date"),
    }
    
    def onchange_category_id(self, cr, uid, ids, category_id, context=None):
        res = super(account_asset_asset, self).onchange_category_id(cr, uid, ids, category_id, context)
        asset_categ_obj = self.pool.get('account.asset.category')
        if category_id:
            category_obj = asset_categ_obj.browse(cr, uid, category_id, context=context)
            res['value']['simple_prorata'] = category_obj.simple_prorata
        return res
        
#end of account_asset_asset()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
