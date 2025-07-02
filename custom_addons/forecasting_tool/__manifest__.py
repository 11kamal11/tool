{
    'name': 'New Forecasting Tool',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'A tool for time series forecasting using Prophet',
    'description': """
        A module to upload CSV files and generate time series forecasts using Prophet.
    """,
    'author': 'Kamal',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/forecast_templates.xml',
        'views/forecast_views.xml',
    ],
    'icon': 'static/description/icon.png',
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}