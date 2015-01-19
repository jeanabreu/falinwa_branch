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

class mrp_production(orm.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    _columns = {
        'fal_sale_id': fields.many2one('sale.order', 'Related Sale Order', help="The sale order related to a MO."), 
        'fal_customer_id': fields.many2one('res.partner', 'Customer'), 
        'fal_currency_id': fields.many2one('res.currency', 'Currency'), 
    }
    
#end of mrp_production()

class procurement_order(orm.Model):
    _name = 'procurement.order'
    _inherit = 'procurement.order'

    def _prepare_mo_vals(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._prepare_mo_vals(cr, uid, procurement, context)
        res['fal_serie_name_id'] = procurement.sale_line_id.fal_serie_name_id.id
        res['fal_ordering_code_id'] = procurement.sale_line_id.fal_ordering_code_id.id
        res['fal_bore_diameter_id'] = procurement.sale_line_id.fal_bore_diameter_id.id
        res['fal_rod_diameter_id'] = procurement.sale_line_id.fal_rod_diameter_id.id
        res['fal_main_option_id'] = procurement.sale_line_id.fal_main_option_id.id
        res['fal_rod_end_id'] = procurement.sale_line_id.fal_rod_end_id.id
        res['fal_rod_end_option_id'] = procurement.sale_line_id.fal_rod_end_option_id.id
        res['fal_seal_kit_id'] = procurement.sale_line_id.fal_seal_kit_id.id
        res['fal_mounting_id'] = procurement.sale_line_id.fal_mounting_id.id
        res['fal_purge'] = procurement.sale_line_id.fal_purge
        res['fal_brace_ring'] = procurement.sale_line_id.fal_brace_ring
        res['fal_counter_bores'] = procurement.sale_line_id.fal_counter_bores
        res['fal_for_handling'] = procurement.sale_line_id.fal_for_handling
        res['fal_microrupteur'] = procurement.sale_line_id.fal_microrupteur
        res['fal_magnet_sensor'] = procurement.sale_line_id.fal_magnet_sensor
        res['fal_xcma'] = procurement.sale_line_id.fal_xcma
        res['fal_cote_x'] = procurement.sale_line_id.fal_cote_x
        res['fal_magnet_sensor_position_id'] = procurement.sale_line_id.fal_magnet_sensor_position_id.id
        res['fal_seal_location'] = procurement.sale_line_id.fal_seal_location
        res['fal_full_reference'] = procurement.sale_line_id.fal_full_reference
        res['fal_sale_reference'] = procurement.sale_line_id.fal_sale_reference
        res['fal_ref_for_stroke_option'] = procurement.sale_line_id.fal_ref_for_stroke_option
        res['fal_by_stroke_option'] = procurement.sale_line_id.fal_by_stroke_option
        res['fal_bom_reference'] = procurement.sale_line_id.fal_bom_reference
        res['fal_ref_priced_option'] = procurement.sale_line_id.fal_ref_priced_option
        res['fal_ref_free_option'] = procurement.sale_line_id.fal_ref_free_option
        res['fal_by_stroke_option'] = procurement.sale_line_id.fal_by_stroke_option
        res['fal_stroke'] = procurement.sale_line_id.fal_stroke
        res['fal_standard_stroke_id'] = procurement.sale_line_id.fal_standard_stroke_id.id
        res['fal_piston_seal'] = procurement.sale_line_id.fal_piston_seal
        res['fal_rod_seal'] = procurement.sale_line_id.fal_rod_seal
        res['fal_ports'] = procurement.sale_line_id.fal_ports
        res['fal_position_ports_head'] = procurement.sale_line_id.fal_position_ports_head
        res['fal_position_ports_bottom'] = procurement.sale_line_id.fal_position_ports_bottom
        res['fal_value_xv'] = procurement.sale_line_id.fal_value_xv
        res['fal_special'] = procurement.sale_line_id.fal_special
        res['fal_y'] = procurement.sale_line_id.fal_y
        res['fal_w'] = procurement.sale_line_id.fal_w
        res['fal_comment_for_vh'] = procurement.sale_line_id.fal_comment_for_vh
        res['fal_sale_id'] = procurement.sale_line_id.order_id.id
        res['fal_customer_id'] = procurement.sale_line_id.order_id.partner_id.id
        res['fal_currency_id'] = procurement.sale_line_id.order_id.currency_id.id
        return res
        
#end of procurement_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
