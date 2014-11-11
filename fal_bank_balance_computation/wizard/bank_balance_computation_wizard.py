from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time

class bank_balance_computation_wizard(orm.TransientModel):
    _name = "bank.balance.computation.wizard"
    _description = "Bank Balance Computation Wizard"

    _columns = {
        'state' : fields.selection([('draft', 'Draft'),('done','Done')], 'Done', required=True),
        'date_start': fields.date('Start Date'),
        'date_stop': fields.date('End Date'),
        'target_moves' : fields.selection([('posted', 'All Posted Entries'),('all','All Entries')], 'Target Moves', required=True), 
        'temp' : fields.one2many('bank.balances.line', 'wizard_id', 'Temp', readonly=True),
    }
    
    def _check_duration(self, cr, uid, ids, context=None):
        obj_fy = self.browse(cr, uid, ids[0], context=context)
        if obj_fy.date_stop < obj_fy.date_start:
            return False
        return True

    _constraints = [
        (_check_duration, 'Error!\nThe start date of a fiscal year must precede its end date.', ['date_start','date_stop'])
    ]
    
    def _get_default_temp(self, cr, uid, ids, target_moves='posted', date_start=False, date_stop=False, context=None):
        if context is None:
            context = {}
        account_obj = self.pool.get('account.account')
        journal_item_obj = self.pool.get('account.move.line')
        bank_account_ids = account_obj.search(cr, uid, [('user_type.code','=','bank')], context=context)
        temp = []
        args = []
        if date_start and date_stop:
            args.append(('date','>=',date_start))
            args.append(('date','<=',date_stop))
        if target_moves == 'posted':
            args.append(('move_id.state','=',target_moves))
        for bank_account_id in account_obj.browse(cr, uid, bank_account_ids, context=context):
            journal_item_ids = journal_item_obj.search(cr, uid, [
                ('account_id','=',bank_account_id.id)]+args, context=context)
            balance_ccr = balance_bcr = 0.00
            for journal_item_id in journal_item_obj.browse(cr, uid, journal_item_ids, context=context):
                if journal_item_id.credit:
                    balance_ccr -= journal_item_id.credit
                else:
                    balance_ccr += journal_item_id.debit
                if bank_account_id.currency_id.id:
                    balance_bcr += journal_item_id.amount_currency
                else:
                    if journal_item_id.credit:
                        balance_bcr -= journal_item_id.credit
                    else:
                        balance_bcr += journal_item_id.debit
            temp.append((0,0,{
                'bank_name_id' : bank_account_id.id,
                'balance_in_company_currency' : balance_ccr,
                'company_currency_id' : bank_account_id.company_id.currency_id.id,
                'balance_in_bank_currency' : balance_bcr,
                'bank_currency_id' : bank_account_id.currency_id and bank_account_id.currency_id.id or bank_account_id.company_id.currency_id.id,
            }))
        return temp

    _defaults = {
        'target_moves' : 'posted',
        'state' : 'draft',
        'temp' : _get_default_temp,
    }
    
    def filter_bank_balance(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0] 
        account_obj = self.pool.get('account.account')
        journal_item_obj = self.pool.get('account.move.line')

        #get temp
        temp = self._get_default_temp(cr, uid, ids, target_moves=data_wizard.target_moves, date_start=data_wizard.date_start, date_stop=data_wizard.date_stop, context=context)

        temp_del = []
        #delete all
        for temp_id in self.browse(cr, uid, ids, context=context)[0].temp:
            temp_del.append((2,temp_id.id))
        self.write(cr, uid, ids, {'temp' : temp_del}, context=context)

        #generate new
        self.write(cr, uid, ids, {
            'temp' : temp,
            'state' : 'done',
        }, context=context)
        
        return {
             'type': 'ir.actions.act_window',
             'name': "Bank Balance",
             'res_model': 'bank.balance.computation.wizard',
             'res_id': ids[0],
             'view_type': 'form',
             'view_mode': 'form',
             'target': 'new',
             'nodestroy': True,
        }
             
#end of bank_balance_computation_wizard()

class bank_balances_line(orm.TransientModel):
    _name = "bank.balances.line"
    _description = "Bank Balances Line"

    _columns = {
        'wizard_id' : fields.many2one('bank.balance.computation.wizard','Wizard'),
        'bank_name_id' : fields.many2one('account.account','Bank Name'),
        'balance_in_company_currency' : fields.float('Balance (CCR)',digits_compute=dp.get_precision('Account')),
        'company_currency_id' : fields.many2one('res.currency', 'Company Currency'),
        'balance_in_bank_currency' : fields.float('Balance (BCR)',digits_compute=dp.get_precision('Account')),
        'bank_currency_id' : fields.many2one('res.currency', 'Bank Currency'),
    }


#end of bank_balances_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
