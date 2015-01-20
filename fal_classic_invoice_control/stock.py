# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from openerp.osv import fields, orm
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


#----------------------------------------------------------
# Stock Picking
#----------------------------------------------------------
class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    

    
#end of stock_picking()