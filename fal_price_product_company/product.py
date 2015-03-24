# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class product_template(models.Model):
    _name = "product.template"
    _inherit = "product.template"
                                
    #fields start here
    #fal_price_product_company_line_ids = fields.One2many('fal.price.product.company.line', 'fal_product_id', string='Price Product Company Line')
    list_price = fields.Float(company_dependent=True)
    #end here
    
#end of product_template()

class fal_price_product_company_line(models.Model):
    _name = "fal.price.product.company.line"
    _description = "Price Product Company"
    
    """                            
    #fields start here
    fal_sale_price = fields.Float('Sale Price', digits_compute=dp.get_precision('Product Price'), help="Base price to compute the customer price. Sometimes called the catalog price.")
    fal_sale_price_currency_id = fields.Many2one('res.currency', string="Sale Currency", help="Select a Sale Currency")
    fal_cost_price = fields.Float('Cost Price', digits_compute=dp.get_precision('Product Price'), help="Base price to compute the customer price. Sometimes called the catalog price.")
    fal_purchase_price_currency_id
    fal_cost_bom_price
    fal_cost_bom_price_currency_id
    fal_net_margin
    fal_net_margin_currency_id
    fal_company_id
    #end here
    """
#end of fal_price_product_company_line()
