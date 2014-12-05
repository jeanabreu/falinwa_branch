# -*- coding: utf-8 -*-

import logging
from openerp import tools

from email.header import decode_header
from openerp import SUPERUSER_ID
from openerp.osv import orm, fields
from openerp.tools import html_email_clean
from openerp.tools.translate import _


class mail_message(orm.Model):
    _name = 'mail.message'
    _inherit = 'mail.message'

    _columns = {
        'company_id' : fields.many2one('res.company', 'Company'),
    }

    _defaults = {
        'company_id' : lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'mail.message', context=c),
    }
#end of mail_message()