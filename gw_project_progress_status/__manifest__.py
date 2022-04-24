# -*- encoding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'Project Progress Status',
    'category': 'project',
    'description': """
        Project Progress Status
        """,
    'author': 'Groway',
    'website': 'http://www.gro-way.com',
    'category': 'Project',
    'version': '1.0',
    'license': 'OPL-1',
    'depends': ['project'],
    'data': [
        'views/project_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
