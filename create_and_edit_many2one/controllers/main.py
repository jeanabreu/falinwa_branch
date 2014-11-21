import openerp
from openerp.addons.web.controllers.main import manifest_list, module_boot

class create_and_edit_many2one(openerp.addons.web.http.Controller):
    _cp_path = '/create_and_edit_many2one'

    @openerp.addons.web.http.jsonrequest
    def create_edit_allowed(self, req):
        Model = req.session.model('res.groups')
        domain = [('name', '=', 'Do not allow Create and Edit')]
        ids = Model.search(domain, 0, False, False, req.context)
        id = ids and ids[0]
        #print "\n\nres group is :::: ",id
        user_model = req.session.model('res.users')
        user_groups = list(set(user_model.read(req.session._uid, ['groups_id'], req.context)['groups_id']))
        #print "\n\nuser_groups are >>> ",user_groups
        if id in user_groups:
            return True
        return False