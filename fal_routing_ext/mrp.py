# -*- coding: utf-8 -*-
import time
from datetime import datetime

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.product import _common

class mrp_routing_workcenter(orm.Model):
    _name = 'mrp.routing.workcenter'
    _inherit = 'mrp.routing.workcenter'
    
    _columns = {
        'fal_extra_operator' : fields.float('Extra operator', required=True),
    }
    _defaults = {
        'fal_extra_operator': lambda *a: 0.0,
    }
#end of mrp_routing_workcenter()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
