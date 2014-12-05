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

    def make_mo(self, cr, uid, ids, context=None):
        mrp_obj = self.pool.get('mrp.production')
        res = super(procurement_order, self).make_mo(cr, uid, ids, context)
        for po in self.browse(cr, uid, ids):
            if po.sale_order_line_id:
                mrp_obj.write(cr, uid, res[po.id], {
                    'fal_serie_name_id': po.sale_order_line_id.fal_serie_name_id.id,
                    'fal_ordering_code_id' : po.sale_order_line_id.fal_ordering_code_id.id,
                    'fal_bore_diameter_id': po.sale_order_line_id.fal_bore_diameter_id.id,
                    'fal_rod_diameter_id' : po.sale_order_line_id.fal_rod_diameter_id.id,
                    'fal_main_option_id': po.sale_order_line_id.fal_main_option_id.id,
                    'fal_rod_end_id': po.sale_order_line_id.fal_rod_end_id.id,
                    'fal_rod_end_option_id' : po.sale_order_line_id.fal_rod_end_option_id.id,
                    'fal_seal_kit_id': po.sale_order_line_id.fal_seal_kit_id.id,
                    'fal_mounting_id': po.sale_order_line_id.fal_mounting_id.id,
                    'fal_purge': po.sale_order_line_id.fal_purge,
                    'fal_brace_ring' : po.sale_order_line_id.fal_brace_ring,
                    'fal_counter_bores': po.sale_order_line_id.fal_counter_bores,
                    'fal_for_handling': po.sale_order_line_id.fal_for_handling,
                    'fal_microrupteur': po.sale_order_line_id.fal_microrupteur,
                    'fal_magnet_sensor': po.sale_order_line_id.fal_magnet_sensor,
                    'fal_xcma' : po.sale_order_line_id.fal_xcma,
                    'fal_cote_x': po.sale_order_line_id.fal_cote_x,
                    'fal_magnet_sensor_position_id': po.sale_order_line_id.fal_magnet_sensor_position_id.id,
                    'fal_seal_location': po.sale_order_line_id.fal_seal_location,
                    'fal_full_reference': po.sale_order_line_id.fal_full_reference,
                    'fal_sale_reference': po.sale_order_line_id.fal_sale_reference,
                    'fal_ref_for_stroke_option': po.sale_order_line_id.fal_ref_for_stroke_option,
                    'fal_by_stroke_option': po.sale_order_line_id.fal_by_stroke_option,
                    'fal_bom_reference': po.sale_order_line_id.fal_bom_reference,
                    'fal_ref_priced_option': po.sale_order_line_id.fal_ref_priced_option,
                    'fal_ref_free_option': po.sale_order_line_id.fal_ref_free_option,
                    'fal_by_stroke_option': po.sale_order_line_id.fal_by_stroke_option,
                    'fal_stroke' : po.sale_order_line_id.fal_stroke,
                    'fal_standard_stroke_id' : po.sale_order_line_id.fal_standard_stroke_id.id,
                    'fal_piston_seal' : po.sale_order_line_id.fal_piston_seal,
                    'fal_rod_seal' : po.sale_order_line_id.fal_rod_seal,
                    'fal_ports' : po.sale_order_line_id.fal_ports,
                    'fal_position_ports_head' : po.sale_order_line_id.fal_position_ports_head,
                    'fal_position_ports_bottom' : po.sale_order_line_id.fal_position_ports_bottom,
                    'fal_value_xv' : po.sale_order_line_id.fal_value_xv,
                    'fal_special' : po.sale_order_line_id.fal_special,
                    'fal_y' : po.sale_order_line_id.fal_y,
                    'fal_w' : po.sale_order_line_id.fal_w,
                    'fal_comment_for_vh' : po.sale_order_line_id.fal_comment_for_vh,
                    'fal_sale_id' : po.sale_order_line_id.order_id.id,
                    'fal_customer_id' : po.sale_order_line_id.order_id.partner_id.id,
                    'fal_currency_id' : po.sale_order_line_id.order_id.currency_id.id,                    
                    })
        return res
        
#end of procurement_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
