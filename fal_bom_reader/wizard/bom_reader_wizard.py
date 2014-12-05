# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class bom_reader_wizard(orm.TransientModel):
    _name = "bom.reader.wizard"
    _description = "BOM Reader Wizard"
    
    _columns = {
        'state': fields.selection([('page1', 'page1'), ('page2', 'page2')], 'State'),
        'ean13': fields.char('EAN13 Barcode', size=13, help="International Article Number used for product identification."),
        'fal_of_number' : fields.char('OF Number',size=64,help="Sequence for Finished Product"),
        'product_id' : fields.many2one('product.product', 'Product', help="Select the product on which want BOM to be view."),
        'temp' : fields.text('temp',readonly=True),
    }
    
    def search_bom(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0] 
        mrp_obj = self.pool.get('mrp.production')
        product_obj = self.pool.get('product.product')
        product_id = False
        if data_wizard.ean13:
            product_ids = product_obj.search(cr, uid, [('ean13', '=', data_wizard.ean13)],limit=1)
            if not product_ids:
                raise orm.except_orm(_("Warning!"), _("Product doesnt exists on this barcode!"))
            for i in product_ids:
                product_id = i
        elif data_wizard.fal_of_number:
            mrp_ids = mrp_obj.search(cr, uid, [('fal_of_number', '=', data_wizard.fal_of_number)],limit=1)
            if not mrp_ids:
                raise orm.except_orm(_("Warning!"), _("Product doesnt exists on this OF Number!"))
            for i in mrp_obj.browse(cr, uid, mrp_ids):
                product_id = i.product_id.id
        elif data_wizard.product_id.id:
            product_id = data_wizard.product_id.id
        else:
            raise orm.except_orm(_("Warning!"), _("Please Provide the Information to search!"))
        return {
            'type': 'ir.actions.act_window',
            'name': data_wizard.product_id.name,
            'res_model': 'mrp.bom',
            'view_mode': 'tree',
            'view_type': 'tree',
            'view_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'mrp', 'mrp_bom_tree_view')[1],
            'domain' : '[("bom_id","=",False),("product_id","=",'+str(product_id)+')]',
            'target': 'new',
             }

    def onchange_ean13(self, cr, uid, ids, ean13, context=None):
        if context is None:
            context = {}
        res = {}
        product_obj = self.pool.get('product.product')
        if ean13:
            product_id = product_obj.search(cr, uid, [('ean13', '=', ean13)],limit=1)
            for i in product_id:
                res['value'] = { 'product_id':i}
        return res

    def onchange_of_number(self, cr, uid, ids, of_number, context=None):
        if context is None:
            context = {}
        res = {}
        mrp_obj = self.pool.get('mrp.production')
        if of_number:
            mrp_ids = mrp_obj.search(cr, uid, [('fal_of_number', '=', of_number)],limit=1)
            for i in mrp_obj.browse(cr, uid, mrp_ids):
                res['value'] = { 'product_id':i.product_id.id}
        return res
        
#end of bom_reader_wizard()