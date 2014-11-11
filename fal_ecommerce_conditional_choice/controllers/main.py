# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.website_sale.controllers.main import website_sale

class falconExtwebsite_sale(website_sale):    

    def get_conditional_choice_values(self, data=None):
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        
        serie_name_obj = registry.get('fal.serie.name')
        bore_diameter_obj = registry.get('fal.bore.diameter')
        main_option_obj = registry.get('fal.main.option')
        road_end_obj = registry.get('fal.road.end')
        seal_kit_obj = registry.get('fal.seal.kit')
        mounting_obj = registry.get('fal.mounting')
                        
        serie_name_ids = serie_name_obj.search(cr, SUPERUSER_ID, [], context=context)
        bore_diameter_ids = bore_diameter_obj.search(cr, SUPERUSER_ID, [], context=context)
        main_option_ids = main_option_obj.search(cr, SUPERUSER_ID, [], context=context)
        road_end_ids = road_end_obj.search(cr, SUPERUSER_ID, [], context=context)
        seal_kit_ids = seal_kit_obj.search(cr, SUPERUSER_ID, [], context=context)
        mounting_ids = mounting_obj.search(cr, SUPERUSER_ID, [], context=context)
        
        serie_names = serie_name_obj.browse(cr, SUPERUSER_ID, serie_name_ids, context)
        bore_diameters = bore_diameter_obj.browse(cr, SUPERUSER_ID, bore_diameter_ids, context)
        main_options = main_option_obj.browse(cr, SUPERUSER_ID, main_option_ids, context)
        road_ends = road_end_obj.browse(cr, SUPERUSER_ID, road_end_ids, context)
        seal_kits = seal_kit_obj.browse(cr, SUPERUSER_ID, seal_kit_ids, context)
        mountings = mounting_obj.browse(cr, SUPERUSER_ID, mounting_ids, context)
       
        return {
            'serie_names': serie_names,
            'bore_diameters': bore_diameters,
            'main_options': main_options,
            'road_ends': road_ends,
            'seal_kits': seal_kits,
            'mountings': mountings,
            'error': {},
            'conditional_choice' : {},
        } 

    @http.route()    
    def shop(self, page=0, category=None, search='', **post):
        res = super(falconExtwebsite_sale, self).shop(page, category, search, **post)
        values = self.get_conditional_choice_values()       
        res.qcontext['serie_names'] = values['serie_names']
        res.qcontext['bore_diameters'] = values['bore_diameters']
        res.qcontext['main_options'] = values['main_options']
        res.qcontext['road_ends'] = values['road_ends']
        res.qcontext['seal_kits'] = values['seal_kits']
        res.qcontext['mountings'] = values['mountings']
        res.qcontext['error'] = values['error']
        res.qcontext['conditional_choice'] = values['conditional_choice']
        return res
    
    @http.route()
    def product(self, product, category='', search='', **kwargs):
        res = super(falconExtwebsite_sale, self).product(product, category, search, **kwargs)
        values = self.get_conditional_choice_values()       
        res.qcontext['serie_names'] = values['serie_names']
        res.qcontext['bore_diameters'] = values['bore_diameters']
        res.qcontext['main_options'] = values['main_options']
        res.qcontext['road_ends'] = values['road_ends']
        res.qcontext['seal_kits'] = values['seal_kits']
        res.qcontext['mountings'] = values['mountings']
        res.qcontext['error'] = values['error']
        res.qcontext['conditional_choice'] = values['conditional_choice']
        return res
        
#end falconExtwebsite_sale class

# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
