# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _

class stock_inventory(models.Model):
    _name = "stock.inventory"
    _inherit = "stock.inventory"
    
    @api.model
    def _get_available_filters(self):
        res = super(stock_inventory, self)._get_available_filters()
        res.append(('by categories', _('By Product Categories')))
        return res
        
    filter = fields.Selection(_get_available_filters, 'Inventory of', required=True,
                                   help="If you do an entire inventory, you can choose 'All Products' and it will prefill the inventory with the current stock.  If you only do some products  "\
                                      "(e.g. Cycle Counting) you can choose 'Manual Selection of Products' and the system won't propose anything.  You can also let the "\
                                      "system propose for a single product / lot /... ")

    fal_internal_category_id = fields.Many2one('product.category','Internal Category')
    
    @api.model
    def _get_inventory_lines_bycategory(self, inventory):
        product_obj = self.env['product.product']
        quant_obj = self.env["stock.quant"]
        vals = []
        product_ids = product_obj.search([('categ_id','child_of', inventory.fal_internal_category_id.id)])
        for product_id in product_ids:
            dom = [('company_id', '=', inventory.company_id.id), ('location_id', '=', inventory.location_id.id),
                            ('product_id','=', product_id.id)]
            quants = quant_obj.search(dom)
            tot_qty = sum([x.qty for x in quants])
            vals.append({
                'inventory_id': inventory.id,
                'location_id': inventory.location_id.id,
                'product_id': product_id.id,
                'product_uom_id': product_id.uom_id.id,
                'product_qty': tot_qty,
            })
        return vals
        
    @api.multi
    def prepare_inventory(self):
        product_obj = self.env['product.product']
        inventory_line_obj = self.env['stock.inventory.line']
        for inventory in self:
            line_ids = [line.id for line in inventory.line_ids]
            if not line_ids and inventory.filter == 'by categories':
                fal_vals = self._get_inventory_lines_bycategory(inventory)
                for fal_product in fal_vals:                
                    inventory_line_obj.create(fal_product)
        return super(stock_inventory, self).prepare_inventory()  
        
#end of stock_inventory()