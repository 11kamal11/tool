from odoo import models, fields

class ForecastResult(models.Model):
    _name = 'forecast.result'
    _description = 'Forecast Result'

    name = fields.Char(string='Name', required=True)
    forecast_data_id = fields.Many2one('forecast.data', string='Forecast Data')
    horizon = fields.Integer(string='Horizon')
    five_year_forecast = fields.Boolean(string='Five Year Forecast')
    yearly_seasonality = fields.Boolean(string='Yearly Seasonality')
    include_holidays = fields.Boolean(string='Include Holidays')
    rmse = fields.Float(string='RMSE')
    mae = fields.Float(string='MAE')
    mape = fields.Float(string='MAPE')
    forecast_lines = fields.One2many('forecast.result.line', 'forecast_result_id', string='Forecast Lines')

    def generate_forecast(self):
        pass  # Implement your forecasting logic here

class ForecastResultLine(models.Model):
    _name = 'forecast.result.line'
    _description = 'Forecast Result Line'

    forecast_result_id = fields.Many2one('forecast.result', string='Forecast Result')
    date = fields.Date(string='Date')
    yhat = fields.Float(string='Forecast Value')
    yhat_lower = fields.Float(string='Lower Bound')
    yhat_upper = fields.Float(string='Upper Bound')