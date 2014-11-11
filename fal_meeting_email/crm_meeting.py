#  -*- coding: utf-8 -*-
import time

from openerp.osv import fields, orm
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.translate import _

class crm_meeting(orm.Model):
    """ Model for CRM meetings """
    _name = 'crm.meeting'
    _inherit = 'crm.meeting'
    
    _columns = {
        'is_send_email' : fields.boolean('Send Invitation Email Automatically?'),
    }
    
    def create_attendees(self, cr, uid, ids, context):
        att_obj = self.pool.get('calendar.attendee')
        user_obj = self.pool.get('res.users')
        current_user = user_obj.browse(cr, uid, uid, context=context)
        for event in self.browse(cr, uid, ids, context):
            if event.is_send_email:
                super(crm_meeting, self).create_attendees(cr, uid, ids, context)
        return True
    
#end of crm_meeting()