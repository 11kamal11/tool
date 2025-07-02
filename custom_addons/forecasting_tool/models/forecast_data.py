from odoo import models, fields

class ForecastData(models.Model):
    _name = 'forecast.data'
    _description = 'Forecast Data'

    name = fields.Char(string='Name', required=True)
    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')
    date_column = fields.Char(string='Date Column')
    target_column = fields.Char(string='Target Column')
    frequency = fields.Selection([
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
    ], string='Frequency')
    data_lines = fields.One2many('forecast.data.line', 'forecast_data_id', string='Data Lines')

class ForecastDataLine(models.Model):
    _name = 'forecast.data.line'
    _description = 'Forecast Data Line'

    forecast_data_id = fields.Many2one('forecast.data', string='Forecast Data')
    date_value = fields.Date(string='Date')
    target_value = fields.Float(string='Target Value')
