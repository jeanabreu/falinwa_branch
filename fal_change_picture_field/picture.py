# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'image': fields.ImageField('Image', help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=128,
            width=128,
            ),
        'image_small': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=64,
            width=64,
            ),
    }
    
#end of product_product()

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'image': fields.ImageField('Image', help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=128,
            width=128,
            ),
        'image_small': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=64,
            width=64,
            ),
    }
    
#end of res_partner()

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'image': fields.ImageField('Image', help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=128,
            width=128,
            ),
        'image_small': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=64,
            width=64,
            ),
    }
    
#end of res_partner()


class hr_employee(orm.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"
    
    _columns = {
        'image': fields.ImageField('Image', help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=128,
            width=128,
            ),
        'image_small': fields.ImageField(
            'Image Medium',
            resize_based_on='image',
            height=64,
            width=64,
            ),
    }
    
#end of hr_employee()