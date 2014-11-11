# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_production_lot(orm.Model):
    _name = 'stock.production.lot'
    _inherit = ['mail.thread', 'ir.needaction_mixin', 'stock.production.lot']    
    
#end of stock_production_lot()