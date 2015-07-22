{
    "name": "ACC-33_Account Full Name Stored",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to display a completed full name of account and its parent name
    """,
    "depends" : ['base', 'account', 'analytic'],
    'init_xml': [],
    'update_xml': [
        'account_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}