from odoo import models, fields
import pandas as pd
from prophet import Prophet
import logging

_logger = logging.getLogger(__name__)

class ForecastResult(models.Model):
    _name = 'new.forecast.result'
    _description = 'New Forecast Result'

    name = fields.Char(string='Name', required=True)
    forecast_data_id = fields.Many2one('new.forecast.data', string='Forecast Data')
    horizon = fields.Integer(string='Horizon', default=30)
    five_year_forecast = fields.Boolean(string='Five Year Forecast')
    yearly_seasonality = fields.Boolean(string='Yearly Seasonality')
    include_holidays = fields.Boolean(string='Include Holidays')
    rmse = fields.Float(string='RMSE')
    mae = fields.Float(string='MAE')
    mape = fields.Float(string='MAPE')
    forecast_lines = fields.One2many('new.forecast.result.line', 'forecast_result_id', string='Forecast Lines')

    def generate_forecast(self):
        try:
            data_lines = self.forecast_data_id.data_lines
            if not data_lines:
                raise ValueError("No data lines found for forecasting.")
            
            df = pd.DataFrame({
                'ds': [line.date_value for line in data_lines],
                'y': [line.target_value for line in data_lines]
            })
            model = Prophet(
                yearly_seasonality=self.yearly_seasonality,
                weekly_seasonality=True,
                daily_seasonality=True
            )
            if self.include_holidays:
                model.add_country_holidays(country_name='US')
            model.fit(df)
            future = model.make_future_dataframe(periods=self.horizon, freq=self.forecast_data_id.frequency)
            forecast = model.predict(future)
            
            self.forecast_lines.unlink()
            for _, row in forecast.tail(self.horizon).iterrows():
                self.forecast_lines.create({
                    'forecast_result_id': self.id,
                    'date': row['ds'],
                    'yhat': row['yhat'],
                    'yhat_lower': row['yhat_lower'],
                    'yhat_upper': row['yhat_upper'],
                })
            _logger.info("Forecast generated successfully for %s", self.name)
        except Exception as e:
            _logger.error("Error generating forecast: %s", str(e))
            raise

class ForecastResultLine(models.Model):
    _name = 'new.forecast.result.line'
    _description = 'New Forecast Result Line'

    forecast_result_id = fields.Many2one('new.forecast.result', string='Forecast Result')
    date = fields.Date(string='Date')
    yhat = fields.Float(string='Forecast Value')
    yhat_lower = fields.Float(string='Lower Bound')
    yhat_upper = fields.Float(string='Upper Bound')