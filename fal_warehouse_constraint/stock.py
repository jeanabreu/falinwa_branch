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


class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    def _check_source_destination_location(self, cr ,uid, ids, context=None):
        for stock_picking in self.browse(cr, uid, ids, context=context):
            temp_source = []
            temp_dest = []
            for move in stock_picking.move_lines:
                if move.location_id.id not in temp_source:
                    temp_source.append(move.location_id.id)
                if move.location_dest_id.id not in temp_dest:
                    temp_dest.append(move.location_dest_id.id)
                if len(temp_source) != 1:
                    return False
                if len(temp_dest) != 1:
                    return False
        return True
        
    _constraints = [
        (_check_source_destination_location, 'Moves must have a same source and destination location on each move', ['move_lines']),
    ]

#end of stock_picking()