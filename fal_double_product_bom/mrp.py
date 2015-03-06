# -*- coding: utf-8 -*-
import time
from datetime import datetime

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.product import _common

class mrp_bom(orm.Model):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'


#end of mrp_bom()

class mrp_production(orm.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    


#end of mrp_production()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
