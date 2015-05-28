# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order_line(orm.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"        
        
    _columns = {
        'fal_serie_name_id' : fields.many2one('fal.serie.name','Serie Name'),
        'fal_serie_name_id_name' : fields.related('fal_serie_name_id', 'name', string="Serie Name", type='char', readonly=True),
        'fal_serie_name_id_type' : fields.related('fal_serie_name_id', 'type', string="Serie Name Type", type='char', readonly=True),
        'fal_ordering_code_id' : fields.many2one('fal.ordering.code','Ordering Code', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_bore_diameter_id' : fields.many2one('fal.bore.diameter','Bore Diameter (mm)', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_rod_diameter_id' : fields.many2one('fal.rod.diameter','Rod Diameter (mm)', domain="[('fal_bore_list_ids','=',fal_bore_diameter_id)]"),
        'fal_main_option_id' : fields.many2one('fal.main.option','Main Option', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_main_option_code' : fields.related('fal_main_option_id', 'code', string="Main Option Code", type='char', readonly=True),
        'fal_rod_end_id' : fields.many2one('fal.rod.end','Rod End', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_rod_end_option_id' : fields.many2one('fal.rod.end.option','Rod End Option'),
        'fal_seal_kit_id' : fields.many2one('fal.seal.kit','Seal Kit', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_mounting_id' : fields.many2one('fal.mounting','Mounting', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_mounting_id_code' : fields.related('fal_mounting_id', 'code', string="Main Option Code", type='char', readonly=True),
        'fal_purge' : fields.boolean('Purge(PG)?'),
        'fal_brace_ring' : fields.boolean('Brace Ring?'),
        'fal_counter_bores' : fields.boolean('Counter Bores(LV)?'),
        'fal_for_handling' : fields.boolean('For Handling(TA)?'),
        'fal_microrupteur' : fields.boolean('Micro Rupteur?'),
        'fal_magnet_sensor' : fields.boolean('Magnet Sensor?'),
        'fal_xcma' : fields.boolean('XCMA 110?'),
        'fal_cote_x' : fields.integer('COTE X', required=True),
        'fal_magnet_sensor_position_id' : fields.many2one('fal.magnet.position', 'Magnet Sensor Position'),
        'fal_seal_location' : fields.char('Seal Location', size=128),
        'fal_full_reference' : fields.char('Full Reference',size=256),
        'fal_sale_reference' : fields.char('Sale Reference', size=256),
        'fal_ref_for_stroke_option' : fields.char('Ref For Stroke Option', size=128),
        'fal_by_stroke_option' : fields.char('By Stroke Option', size=128),
        'fal_bom_reference' : fields.char('BOM Reference',size=128),
        'fal_ref_priced_option' : fields.char('Ref Priced Option',size=128),
        'fal_ref_free_option' : fields.char('Ref Free Option',size=128),
        'fal_standard_stroke_id' : fields.many2one('fal.standard.stroke', string='Standard Stroke(mm)'),
        'fal_piston_seal': fields.selection([('D','D - Double acting seal'), ('P','P - Compound Seal')], string='Piston Seal'),
        'fal_rod_seal': fields.selection([('J','J - Single lip seal'), ('P','P - Compound Seal')], string='Rod Seal'),
        'fal_ports': fields.selection([('G','G - Internal Thread Gaz')], string='Ports'),
        'fal_position_ports_head': fields.selection([('1','1'),('2','2'),('3','3'),('4','4'),], string='Position of Ports - Head'),
        'fal_position_ports_bottom': fields.selection([('1','1'),('2','2'),('3','3'),('4','4'),], string='Position of Ports - Bottom'),
        'fal_value_xv' : fields.float('Value for XV (for MT4?DT4 only)'),
        'fal_single_or_double_rod' : fields.related('fal_mounting_id','sr_or_dr',type='char', string='Single or Double Rod', readonly=True),
        'fal_special' : fields.boolean('Special'),
        'fal_y' : fields.float('Y'),
        'fal_w' : fields.float('W'),
        'fal_comment_for_vh' : fields.text('Comment'),
        'fal_stroke' : fields.integer('Stroke (mm)'),
    }

    def get_by_stroke_option(self, cr, uid, ref, fal_stroke):
        stroke_max_obj = self.pool.get('fal.stroke.max')
        by_stroke_option = 'X'
        stroke_max_ids = stroke_max_obj.search(cr, uid, [('name','=',ref)])
        if stroke_max_ids:
            stroke_id = stroke_max_obj.browse(cr, uid, stroke_max_ids[0])
            if stroke_id.a_min != 'NO':
                if fal_stroke < int(stroke_id.a_min):
                    return 'STROKE TOO SHORT'                
                elif fal_stroke <= int(stroke_id.a_max):
                    return 'A'
            if stroke_id.b_min != 'NO':
                if fal_stroke < int(stroke_id.b_min):
                    return 'STROKE TOO SHORT'                    
                elif stroke_id.b_max == 'NO SUP' or fal_stroke <= int(stroke_id.b_max):
                    return 'B'                    
            if stroke_id.c_min != 'NO':
                if fal_stroke < int(stroke_id.c_min):
                    return 'STROKE TOO SHORT'                
                elif fal_stroke >= int(stroke_id.c_min):
                    return 'C'                    
        return by_stroke_option
        
    def onchange_conditional(self, cr, uid, ids, 
        fal_serie_name_id, fal_bore_diameter_id, fal_rod_diameter_id, fal_stroke, fal_main_option_id, fal_rod_end_id, fal_rod_end_option_id, fal_seal_kit_id, fal_mounting_id, 
        fal_purge, fal_counter_bores, fal_for_handling, fal_microrupteur, fal_magnet_sensor, fal_cote_x, fal_magnet_sensor_position_id, fal_seal_location, fal_ordering_code_id, 
        fal_standard_stroke_id, fal_piston_seal, fal_rod_seal, fal_ports, fal_brace_ring, fal_position_ports_head, fal_position_ports_bottom, fal_value_xv, flag=False):
        
        res = {'value': {
            'fal_serie_name_id_name' : '',
            'fal_serie_name_id_type' : '',
            'fal_main_option_code': '',
            'fal_mounting_id_code': '',
            'fal_full_reference': '', 
            'fal_sale_reference': '',
            'fal_ref_for_stroke_option': '',
            'fal_by_stroke_option': '',
            'fal_bom_reference':'', 
            'fal_ref_priced_option':'', 
            'fal_ref_free_option':'',
            'fal_single_or_double_rod':'',
            }}
            
        serie_name = 'XXX'
        bore_diameter = 'XXX' 
        bore_diameter_sale_reference = ''
        sale_ref_bore_diameter = ''
        main_option = 'XX'
        main_option_sale_reference = ''
        rod_end = 'XX'
        rod_end_sale_reference = ''
        seal_kit = 'XX'
        seal_kit_sale_reference = ''
        mounting = 'XXX'
        mounting_sale_reference = ''
        purge = 'NP'
        purge_sale_reference = ''
        counter_bores = 'NL'
        counter_bores_sale_reference = ''
        for_handling = 'NT'
        for_handling_sale_reference = ''
        microrupteur = 'NC'
        magnet_sensor = 'NS'
        magnet_sensor_position = 'XX'
        magnet_sensor_position_sale_ref = ''
        seal_location = 'XX'
        stroke_ref = '000'
        cote_x_ref = '000'
        serie_name_id_type = ''
        fal_standard_stroke_name = ''
        fal_standard_stroke_value = ''
        main_option1 = ''
        main_option2 = ''
        rod_diameter = ''
        rod_end_option = ''
        piston_seal = rod_seal = ports = position_ports_head = position_ports_bottom = 'X'
        brace_ring = 'S'
        value_xv = 'XXX'
        mounting_single_or_double = ''
        sale_ref_rod_diameter = ''
        serie_name_id = False
        rod_type = 'S'
        main_option_sale_ref = ''
        sale_ref_bore_diameter_hvb = ''
        rod_end_sale_refh160 = ''
        mounting_sale_referenceh160 = ''
        
        if fal_serie_name_id:
            serie_name_id = self.pool.get('fal.serie.name').browse(cr, uid, fal_serie_name_id)
            res['value']['fal_serie_name_id_name'] = serie_name = serie_name_id.name
            res['value']['fal_serie_name_id_type'] = serie_name_id_type = serie_name_id.type
        if flag:
            return {'value': {
            'fal_serie_name_id_name' : res['value']['fal_serie_name_id_name'],
            'fal_serie_name_id_type' : res['value']['fal_serie_name_id_type'],
            'fal_ordering_code_id' : False,
            'fal_bore_diameter_id' : False,
            'fal_rod_diameter_id' : False,
            'fal_main_option_id' : False,
            'fal_rod_end_id' : False,
            'fal_rod_end_option_id' : False,
            'fal_seal_kit_id' : False,
            'fal_mounting_id': False,
            'fal_purge': False,
            'fal_brace_ring': False,
            'fal_counter_bores': False,
            'fal_for_handling': False,
            'fal_microrupteur': False,
            'fal_magnet_sensor': False,
            'fal_xcma': False,
            'fal_stroke': 0,
            'fal_cote_x': 0,
            'fal_magnet_sensor_position_id': False,
            'fal_main_option_code': '',
            'fal_mounting_id_code': '',
            'fal_seal_location': '',
            'fal_full_reference': '', 
            'fal_sale_reference': '',
            'fal_ref_for_stroke_option': '',
            'fal_by_stroke_option': '',
            'fal_bom_reference':'', 
            'fal_ref_priced_option':'', 
            'fal_ref_free_option':'',
            'fal_single_or_double_rod':'',
            'fal_piston_seal': '',
            'fal_rod_seal' : '',
            'fal_ports' : '',
            'fal_position_ports_head' : '',
            'fal_position_ports_bottom' : '',
            'fal_value_xv' : 0,
            'fal_special': False,
            'fal_y': 0,
            'fal_w' : 0,
            'fal_comment_for_vh' : '',
            }}
            
        if fal_standard_stroke_id:
            fal_standard_stroke = self.pool.get('fal.standard.stroke').browse(cr, uid, fal_standard_stroke_id)
            fal_standard_stroke_name = fal_standard_stroke.name
            fal_standard_stroke_value = fal_standard_stroke.value
        
        if fal_bore_diameter_id:
            bore_diameter = self.pool.get('fal.bore.diameter').browse(cr, uid, fal_bore_diameter_id).name           
            sale_ref_bore_diameter = bore_diameter
            if bore_diameter[0] == '0':
                sale_ref_bore_diameter = bore_diameter[1:]
            if sale_ref_bore_diameter == '25': 
                sale_ref_bore_diameter_hvb = '02'
            elif sale_ref_bore_diameter == '32': 
                sale_ref_bore_diameter_hvb = '03'
            elif sale_ref_bore_diameter == '40': 
                sale_ref_bore_diameter_hvb = '04'
            elif sale_ref_bore_diameter == '50': 
                sale_ref_bore_diameter_hvb = '05'
            elif sale_ref_bore_diameter == '63': 
                sale_ref_bore_diameter_hvb = '06'
            elif sale_ref_bore_diameter == '80': 
                sale_ref_bore_diameter_hvb = '08'
            elif sale_ref_bore_diameter == '100': 
                sale_ref_bore_diameter_hvb = '10'
            elif sale_ref_bore_diameter == '125': 
                sale_ref_bore_diameter_hvb = '12'
                
        if fal_rod_diameter_id:
            rod_diameter = self.pool.get('fal.rod.diameter').browse(cr, uid, fal_rod_diameter_id).name
            sale_ref_rod_diameter = rod_diameter
            if rod_diameter[0] == '0':
                sale_ref_rod_diameter = rod_diameter[1:]

        if fal_main_option_id:
            main_option = self.pool.get('fal.main.option').browse(cr, uid, fal_main_option_id).code
            if serie_name in ['VBG', 'VCN', 'VCR']:
                main_option_sale_reference = 'MS'
            elif serie_name in ['VPC', 'VXP']:
                main_option_sale_reference = 'ML'
            elif serie_name_id_type == 'B':
                if main_option == 'L2':                    
                    main_option_sale_reference = 2
                elif main_option == 'L3':       
                    main_option_sale_reference = 3
                elif main_option == 'L4':       
                    main_option_sale_reference = 2
                else:
                    main_option_sale_reference = 0
            elif serie_name_id_type == 'H':
                if main_option == 'L2':                    
                    main_option_sale_reference = 3
                elif main_option == 'L3':       
                    main_option_sale_reference = 1
                elif main_option == 'L4':       
                    main_option_sale_reference = 2
                else:
                    main_option_sale_reference = 0
            if main_option != 'DM':
                res['value']['fal_magnet_sensor_position_id'] = False
            res['value']['fal_main_option_code'] = main_option
        else:
            res['value']['fal_magnet_sensor_position_id'] = False
            
        if fal_rod_end_id:
            rod_end = self.pool.get('fal.rod.end').browse(cr, uid, fal_rod_end_id).code
            if serie_name in ['VBG', 'VCN', 'VCR', 'VPC', 'VXP']:
                rod_end_sale_reference = self.pool.get('fal.rod.end').browse(cr, uid, fal_rod_end_id).v_ref
            else:
                rod_end_sale_reference = self.pool.get('fal.rod.end').browse(cr, uid, fal_rod_end_id).vbl_ref
            if rod_end == 'KK':
                rod_end_sale_refh160 =  'KK'
            elif rod_end == 'K1':
                rod_end_sale_refh160 =  'KK1'
            elif rod_end == 'TN':
                rod_end_sale_refh160 =  'T'
        if fal_rod_end_option_id:
            rod_end_option = self.pool.get('fal.rod.end.option').browse(cr, uid, fal_rod_end_option_id).code
        
        if fal_seal_kit_id:
            seal_kit = self.pool.get('fal.seal.kit').browse(cr, uid, fal_seal_kit_id).code
            if serie_name in ['VBG', 'VCN', 'VCR', 'VPC', 'VXP']:
                seal_kit_sale_reference = self.pool.get('fal.seal.kit').browse(cr, uid, fal_seal_kit_id).v_ref
            else:
                seal_kit_sale_reference = self.pool.get('fal.seal.kit').browse(cr, uid, fal_seal_kit_id).vbl_ref
        if fal_mounting_id:
            mounting_id = self.pool.get('fal.mounting').browse(cr, uid, fal_mounting_id)
            mounting = mounting_id.name              
            mounting_sale_reference = mounting_id.code
            if mounting_sale_reference[0] == 'D':
                mounting_sale_referenceh160 = 'M'+mounting_sale_reference
            else:
                mounting_sale_referenceh160 = mounting_sale_reference
            mounting_single_or_double = mounting_id.sr_or_dr or ''
            res['value']['fal_mounting_id_code'] = mounting_id.code
        
        if fal_purge:
            purge = 'PU'
            if serie_name in ['VBG', 'VCN', 'VCR', 'VPC', 'VXP']:
                purge_sale_reference = 'PG'
        
        if fal_counter_bores:
           counter_bores = 'LM'
           if serie_name in ['VBG', 'VCN', 'VCR', 'VPC', 'VXP']:
                counter_bores_sale_reference = 'LV'
        
        if fal_for_handling:
           for_handling = 'TR'
           if serie_name in ['VBG', 'VCN', 'VCR', 'VPC', 'VXP']:
                for_handling_sale_reference = 'TA'
        
        if fal_microrupteur:
            microrupteur = 'MC'
        
        if fal_magnet_sensor:
            magnet_sensor = 'MS'
        
        if fal_magnet_sensor_position_id:
            magnet_sensor_position = magnet_sensor_position_sale_ref = self.pool.get('fal.magnet.position').browse(cr, uid, fal_magnet_sensor_position_id).name
        
        if fal_seal_location:
            seal_location = fal_seal_location

        if fal_piston_seal:
            piston_seal = fal_piston_seal
            
        if fal_rod_seal:
            rod_seal = fal_rod_seal
            
        if fal_ports:
            ports = fal_ports
            
        if fal_brace_ring:
            brace_ring = 'E'
            
        if fal_position_ports_head:
            position_ports_head = fal_position_ports_head
            
        if fal_position_ports_bottom:
            position_ports_bottom = fal_position_ports_bottom
                    
        if bore_diameter!='XXX':
            bore_diameter_sale_reference = int(bore_diameter)

        if main_option == 'DM':
            main_option2 = 'DM'
        else:
            main_option2 = ''
        if main_option == 'IR':
            rod_type = 'D'
        if main_option in ['IR','DM','L1']:
            main_option_sale_ref = 'L1'
        else:
            main_option_sale_ref = main_option
        if fal_stroke:
            if len(str(fal_stroke)) == 1:
                stroke_ref = "00"+str(fal_stroke)
            elif len(str(fal_stroke)) == 2:
                stroke_ref = "0"+str(fal_stroke)
            else:
                stroke_ref = str(fal_stroke)
                
        if fal_cote_x:
            if len(str(fal_cote_x)) == 1:
                cote_x_ref = "00"+str(fal_cote_x)
            elif len(str(fal_cote_x)) == 2:
                cote_x_ref = "0"+str(fal_cote_x)
            else:
                cote_x_ref = str(fal_cote_x)
        
        if fal_value_xv:
            if len(str(fal_value_xv)) == 1:
                value_xv = "00"+str(fal_value_xv)
            elif len(str(fal_cote_x)) == 2:
                value_xv = "0"+str(fal_value_xv)
            else:
                value_xv = str(fal_value_xv)
        
        if serie_name_id and serie_name_id.name == 'H160':
            res['value']['fal_piston_seal'] = 'D'
            res['value']['fal_rod_seal'] = 'J'
            res['value']['fal_ports'] = 'G'
        
        if fal_ordering_code_id:
            ordering_code_id = self.pool.get('fal.ordering.code').browse(cr, uid, fal_ordering_code_id)
            res['value']['fal_stroke'] = ordering_code_id.fal_stroke
            
            if serie_name_id_type == 'V24':
                v24bore_diameter_ids = self.pool.get('fal.bore.diameter').search(cr ,uid, [('name', '=', ordering_code_id.fal_full_reference[4:7])])
                v24main_option_ids = self.pool.get('fal.main.option').search(cr ,uid, [('code', '=', ordering_code_id.fal_full_reference[8:10])])
                v24rod_end_ids = self.pool.get('fal.rod.end').search(cr ,uid, [('code', '=', ordering_code_id.fal_full_reference[11:13])])
                v24seal_kit_ids = self.pool.get('fal.seal.kit').search(cr ,uid, [('code', '=', ordering_code_id.fal_full_reference[14:16])])
                v24mounting_ids = self.pool.get('fal.mounting').search(cr ,uid, [('name', '=', ordering_code_id.fal_full_reference[17:20])])
                res['value']['fal_bore_diameter_id'] = v24bore_diameter_ids and v24bore_diameter_ids[0]
                res['value']['fal_main_option_id'] = v24main_option_ids and v24main_option_ids[0]
                res['value']['fal_rod_end_id'] = v24rod_end_ids and v24rod_end_ids[0]
                res['value']['fal_seal_kit_id'] = v24seal_kit_ids and v24seal_kit_ids[0]
                res['value']['fal_mounting_id'] = v24mounting_ids and v24mounting_ids[0]
                res['value']['fal_full_reference'] = ordering_code_id.name
                res['value']['fal_bom_reference'] = ordering_code_id.name
                res['value']['fal_cote_x'] = 0
                if ordering_code_id.fal_full_reference[4:7] in ['040','050']:                    
                    res['value']['fal_cote_x'] = 60
                else:
                    res['value']['fal_cote_x'] = 72
                
                if serie_name_id.name == 'INT_V24':
                    res['value']['fal_full_reference'] = "INT_" + res['value']['fal_full_reference']
                    res['value']['fal_bom_reference'] = "INT_" + res['value']['fal_bom_reference']
                #res['value']['fal_ref_priced_option'] = ordering_code_id.fal_full_reference[23:41]
                #res['value']['fal_ref_free_option'] = ordering_code_id.fal_full_reference[42:]
            
            if serie_name_id_type == 'V72':
                ful_ref_obj = self.pool.get('fal.ref.data')
                res['value']['fal_ref_for_stroke_option'] = '%s-%s-%s' %(ordering_code_id.name, rod_end, mounting)
                ful_ref = ''
                ful_ref_ids = ful_ref_obj.search(cr, uid, [('name','=',res['value']['fal_ref_for_stroke_option'])])
                if ful_ref_ids:
                    ful_ref = ful_ref_obj.browse(cr, uid, ful_ref_ids[0]).value
                v72bore_diameter_ids = self.pool.get('fal.bore.diameter').search(cr ,uid, [('name', '=', ful_ref[4:7])])
                v72main_option_ids = self.pool.get('fal.main.option').search(cr ,uid, [('code', '=', ful_ref[8:10])])
                v72rod_end_ids = self.pool.get('fal.rod.end').search(cr ,uid, [('code', '=', ful_ref[11:13])])
                v72seal_kit_ids = self.pool.get('fal.seal.kit').search(cr ,uid, [('code', '=', ful_ref[14:16])])
                v72mounting_ids = self.pool.get('fal.mounting').search(cr ,uid, [('code', '=', ful_ref[17:20])])
                res['value']['fal_bore_diameter_id'] = v72bore_diameter_ids and v72bore_diameter_ids[0]
                res['value']['fal_main_option_id'] = v72main_option_ids and v72main_option_ids[0]
                res['value']['fal_seal_kit_id'] = v72seal_kit_ids and v72seal_kit_ids[0]
                res['value']['fal_full_reference'] = '%s-%s-%s' %(ordering_code_id.name, rod_end, mounting)
                res['value']['fal_bom_reference'] = '%s-%s-%s' %(ordering_code_id.name, rod_end, mounting)
                res['value']['fal_cote_x'] = 0
                if serie_name_id.name == 'INT_V72':
                    res['value']['fal_full_reference'] = "INT_" + res['value']['fal_full_reference']
                    res['value']['fal_bom_reference'] = "INT_" + res['value']['fal_bom_reference']
                    res['value']['fal_ref_for_stroke_option'] = "INT_" + res['value']['fal_ref_for_stroke_option']
                #if ful_ref[4:7] in ['040','050']:                    
                #    res['value']['fal_cote_x'] = 60
                #else:
                #    res['value']['fal_cote_x'] = 72
                    
                #res['value']['fal_ref_priced_option'] = ful_ref[23:41]
                #res['value']['fal_ref_free_option'] = ful_ref[42:]
            res['value']['fal_sale_reference'] = ordering_code_id.name.replace('-',' ')
            if serie_name_id.name in ['INT_V72','INT_V24']:
                res['value']['fal_sale_reference'] = "INT_" + res['value']['fal_sale_reference']
            return res
        
        if serie_name in ['VPC', 'VXP']:
            res['value']['fal_sale_reference'] = '%s %s %s %s %s %s %s %s %s %s %s %s %s %s' %(serie_name, sale_ref_bore_diameter, main_option_sale_reference, rod_end_sale_reference, seal_kit_sale_reference, fal_stroke, rod_type, mounting_sale_reference, main_option_sale_ref, main_option2, magnet_sensor_position_sale_ref, purge_sale_reference, counter_bores_sale_reference, for_handling_sale_reference)
        elif serie_name in ['VCN','VBG','VCR']:
            res['value']['fal_sale_reference'] = '%s %s %s %s %s %s %s %s %s %s %s %s %s %s' %(serie_name, sale_ref_bore_diameter, main_option_sale_reference, rod_end_sale_reference, seal_kit_sale_reference, fal_stroke, rod_type, str(fal_cote_x), mounting_sale_reference, main_option_sale_ref, main_option2, purge_sale_reference, counter_bores_sale_reference, for_handling_sale_reference)     
        elif serie_name == 'VBM':
            res['value']['fal_sale_reference'] = '%s %s %s %s %s %s %s' %(serie_name, sale_ref_bore_diameter, mounting_sale_reference, rod_end_sale_reference, seal_kit_sale_reference, str(fal_stroke), magnet_sensor_position_sale_ref)
        elif serie_name_id_type == 'H':
            res['value']['fal_sale_reference'] = '%s %s %s %s %s%s%s%s %s %s %s %s %s %s %s %s %s' %(serie_name + 'CO', sale_ref_bore_diameter, sale_ref_rod_diameter, mounting_sale_referenceh160, seal_kit[1:2], piston_seal, rod_seal, main_option_sale_reference, ports, str(fal_stroke), brace_ring, rod_end_sale_refh160, rod_end_option, position_ports_head, position_ports_bottom, fal_value_xv or '', main_option2)
        else:
            res['value']['fal_sale_reference'] = '%s %s %s %s%s %s %s %s' %(serie_name, sale_ref_bore_diameter, mounting_sale_reference, rod_end_sale_reference, seal_kit_sale_reference, main_option, for_handling_sale_reference, str(fal_stroke))
            
        if serie_name_id_type == 'B':
            res['value']['fal_bom_reference'] = '%s-%s-%s-%s-%s-%s' %(serie_name, bore_diameter, main_option, rod_end, seal_kit, mounting_sale_reference)
            res['value']['fal_full_reference'] = '%s-%s-%s' %(res['value']['fal_bom_reference'], fal_standard_stroke_name, stroke_ref)
            if main_option == 'IR' :
                main_option1 = 'D'
            else:
                main_option1 = 'S'
            if rod_end == 'ET':
                if mounting_sale_reference == 'MBC':
                    mounting = 1
                elif mounting_sale_reference == 'MFF':
                    mounting = 2
                if mounting_sale_reference == 'MLH':
                    mounting = 3
                elif mounting_sale_reference == 'MRE':
                    mounting = 4
            else:
                if mounting_sale_reference == 'MBC':
                    mounting = 5
                elif mounting_sale_reference == 'MFF':
                    mounting = 6
                if mounting_sale_reference == 'MLH':
                    mounting = 7
                elif mounting_sale_reference == 'MRE':
                    mounting = 8
            if seal_kit == 'KN':
                seal_kit = 'H'
            elif seal_kit == 'KV':
                seal_kit = 'V'
            else:
                seal_kit = ''
            res['value']['fal_sale_reference'] = '%s%s %s %s %s %s %s' %(serie_name, main_option1, sale_ref_bore_diameter_hvb, fal_stroke, mounting, seal_kit, main_option2)
            return res        
        elif serie_name_id_type == 'H':
            res['value']['fal_single_or_double_rod'] = mounting_single_or_double
            res['value']['fal_bom_reference'] = '%s-%s-%s-%s-%s-%s-%s' %(serie_name, bore_diameter, rod_diameter, mounting_sale_reference, main_option, rod_end, seal_kit)
            res['value']['fal_ref_priced_option'] = '%s-%s' %(stroke_ref, rod_end_option)
            res['value']['fal_ref_free_option'] = '%s-%s-%s-%s-%s-%s-%s' %(piston_seal, rod_seal, ports, brace_ring, position_ports_head, position_ports_bottom, value_xv)
            
            res['value']['fal_full_reference'] = '%s_%s_%s' %(res['value']['fal_bom_reference'], res['value']['fal_ref_priced_option'], res['value']['fal_ref_free_option'])
            return res
        
        res['value']['fal_ref_for_stroke_option'] = '%s-%s-%s-%s' %(serie_name, bore_diameter, main_option, mounting)            
        res['value']['fal_by_stroke_option'] = self.get_by_stroke_option(cr, uid, res['value']['fal_ref_for_stroke_option'], fal_stroke)
        res['value']['fal_bom_reference'] = '%s-%s-%s-%s-%s-%s-%s' %(serie_name, bore_diameter, main_option, rod_end, seal_kit, mounting, res['value']['fal_by_stroke_option'])
        res['value']['fal_ref_priced_option'] = '%s-%s-%s-%s-%s-%s' %(stroke_ref, purge, counter_bores, for_handling, microrupteur, magnet_sensor)
        res['value']['fal_ref_free_option'] = '%s-%s-%s' %(cote_x_ref, seal_location, magnet_sensor_position)
        
        res['value']['fal_full_reference'] = '%s_%s_%s' %(res['value']['fal_bom_reference'], res['value']['fal_ref_priced_option'], res['value']['fal_ref_free_option'])
        return res      
    
    def fal_sale_ref_change(self, cr, uid, ids, fal_sale_reference):
        res = {'value': {
            'name': False
            }}        
                
        if fal_sale_reference:
            res['value']['name'] = fal_sale_reference
        return res        
    
    def onchange_bomref(self, cr, uid, ids, fal_bom_reference):
        res = {'value': {
            'product_id': False
            }}        
                
        if fal_bom_reference:
            product = self.pool.get('product.product').search(cr, uid, [('name','=', fal_bom_reference)])
            if product:
                res['value']['product_id'] = product[0]
        return res

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        return super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id, lang, update_tax, date_order, packaging, fiscal_position, True, context)
            
#end of sale_order_line()

class fal_serie_name(orm.Model):
    _name = "fal.serie.name"
    _description = "Falinwa Serie Name"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'type' : fields.selection([('V','V'), ('V24','V24'), ('V72','V72'), ('B','B'), ('H','H')], string="Type", required=True),
        'fal_bore_list_ids' : fields.many2many('fal.bore.diameter', 'fal_serie_bore_rel', 'fal_serie_id', 'fal_bore_id', 'Bore List'),
        'fal_main_option_list_ids' : fields.many2many('fal.main.option', 'fal_serie_mainoption_rel', 'fal_serie_id', 'fal_main_option_id', 'Main Option List'),
        'fal_rod_end_list_ids' : fields.many2many('fal.rod.end', 'fal_serie_rod_end_rel', 'fal_serie_id', 'fal_rod_end_id', 'Rod End List'),
        'fal_seal_kit_list_ids' : fields.many2many('fal.seal.kit', 'fal_serie_seal_kit_rel', 'fal_serie_id', 'fal_seal_kit_id', 'Seal Kit List'),
        'fal_mounting_list_ids' : fields.many2many('fal.mounting', 'fal_serie_mounting_rel', 'fal_serie_id', 'fal_mounting_id', 'Mounting List'),
        'fal_ordering_code_list_ids' : fields.many2many('fal.ordering.code', 'fal_serie_ordering_code_rel', 'fal_serie_id', 'fal_ordering_code_id', 'Ordering Code List'),
    }
    
#end of fal_serie_name()

class fal_bore_diameter(orm.Model):
    _name = "fal.bore.diameter"
    _description = "Falinwa Bore Diameter"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'fal_serie_list_ids' : fields.many2many('fal.serie.name', 'fal_serie_bore_rel', 'fal_bore_id', 'fal_serie_id', 'Serie List'),
        'fal_rod_list_ids' : fields.many2many('fal.rod.diameter', 'fal_bore_rod_rel', 'fal_bore_id', 'fal_rod_id', 'Rod List'),
    }
    
#end of fal_bore_diameter()

class fal_rod_diameter(orm.Model):
    _name = "fal.rod.diameter"
    _description = "Falinwa Rod Diameter"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'fal_bore_list_ids' : fields.many2many('fal.bore.diameter', 'fal_bore_rod_rel', 'fal_rod_id', 'fal_bore_id', 'Bore List'),
    }
    
#end of fal_rod_diameter()

class fal_main_option(orm.Model):
    _name = "fal.main.option"
    _description = "Falinwa Main Option"
    
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(cr, uid, ['|',('name', operator, name),('code', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
        
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'code' : fields.char('Code', size=64, required=True),
        'old_code' : fields.char('Old Code', size=64),
        'chinese_name' : fields.char('Chinese Name', size=128),
        'fal_serie_list_ids' : fields.many2many('fal.serie.name', 'fal_serie_mainoption_rel', 'fal_main_option_id', 'fal_serie_id', 'Serie List'),
    }
    
#end of fal_main_option()

class fal_rod_end(orm.Model):
    _name = "fal.rod.end"
    _description = "Falinwa Rod End"

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(cr, uid, ['|',('name', operator, name),('code', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'code' : fields.char('Code', size=64, required=True),
        'vbl_ref' : fields.char('VBL Sales ref', size=64),
        'v_ref' : fields.char('V Sales ref', size=64),
        'chinese_name' : fields.char('Chinese Name', size=128),
        'fal_serie_list_ids' : fields.many2many('fal.serie.name', 'fal_serie_rod_end_rel', 'fal_rod_end_id', 'fal_serie_id', 'Serie List'),
    }
    
#end of fal_rod_end()

class fal_rod_end_option(orm.Model):
    _name = "fal.rod.end.option"
    _description = "Falinwa Rod End Option"

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(cr, uid, ['|',('name', operator, name),('code', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'code' : fields.char('Code', size=64, required=True),
        'ref' : fields.char('Ref', size=64),
        'chinese_name' : fields.char('Chinese Name', size=128),
    }
    
#fal_rod_end_option()

class fal_seal_kit(orm.Model):
    _name = "fal.seal.kit"
    _description = "Falinwa Seal Kit"

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            ids = self.search(cr, uid, ['|',('name', operator, name),('code', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'code' : fields.char('Code', size=64, required=True),
        'vbl_ref' : fields.char('VBL Sales ref', size=64),
        'v_ref' : fields.char('V Sales ref', size=64),
        'chinese_name' : fields.char('Chinese Name', size=128),
        'fal_serie_list_ids' : fields.many2many('fal.serie.name', 'fal_serie_seal_kit_rel', 'fal_seal_kit_id', 'fal_serie_id', 'Serie List'),
    }
    
#end of fal_seal_kit()

class fal_mounting(orm.Model):
    _name = "fal.mounting"
    _description = "Falinwa Mounting"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'code' : fields.char('Code', size=64),
        'sr_or_dr' : fields.char('SR or DR', size=64),
        'fal_serie_list_ids' : fields.many2many('fal.serie.name', 'fal_serie_mounting_rel', 'fal_mounting_id', 'fal_serie_id', 'Serie List'),
    }
    
#end of fal_mounting()

class fal_ordering_code(orm.Model):
    _name = "fal.ordering.code"
    _description = "Falinwa Ordering Code"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'fal_stroke' : fields.float('Stroke'),
        'fal_full_reference' : fields.char('Full Reference',size=128),
        'fal_serie_list_ids' : fields.many2many('fal.serie.name', 'fal_serie_ordering_code_rel', 'fal_ordering_code_id', 'fal_serie_id', 'Ordering Code'),
    }
    
#end of fal_mounting()

class fal_magnet_position(orm.Model):
    _name = "fal.magnet.position"
    _description = "Falinwa Magnet Position"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
    }
    
#end of fal_magnet_position()

class fal_stroke_max(orm.Model):
    _name = "fal.stroke.max"
    _description = "Falinwa Stroke Max"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'a_min' : fields.char('A Min', size=64),
        'a_max' : fields.char('A Max', size=64),
        'b_min' : fields.char('B Min', size=64),
        'b_max' : fields.char('B Max', size=64),
        'c_min' : fields.char('C Min', size=64),
    }
    
#end of fal_stroke_max()

class fal_ref_data(orm.Model):
    _name = "fal.ref.data"
    _description = "Falinwa reference data"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'value' : fields.char('Value', size=128, required=True),
    }
    
#end of fal_ref_data()

class fal_standard_stroke(orm.Model):
    _name = "fal.standard.stroke"
    _description = "Falinwa Standard Stroke"
    
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
        'value' : fields.char('Value', size=128, required=True),
    }
    
#end of fal_standard_stroke()