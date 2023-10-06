{
    'name': 'Appoinment Management',
    'version': '1.0',
    'summary': 'My Custom Doctor-Training Module',
    'category': 'Uncategorized',
    'author': 'İloş Kuran',
    'website': 'http://www.yourwebsite.com',
    'depends': ['base', 'mail'],
    'data': ['views/doctor.xml',
             'security/ir.model.access.csv',
             'views/department.xml',
             'views/patient.xml',
             'views/appointment.xml',
             'views/treatment.xml',
             'views/wizard.xml',
             ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
