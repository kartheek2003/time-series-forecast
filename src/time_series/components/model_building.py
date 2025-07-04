import os
import pandas as pd
from pmdarima import auto_arima
from prophet import Prophet 
import numpy as np
from sklearn.metrics import mean_squared_error
import joblib
import matplotlib.pyplot as plt
from src.time_series.logger import logger
from src.time_series.entity.config_entity import Model


class ModelBuildingComponent:
    def __init__(self, config= Model):
        self.config = config

    def load_data(self):
        if not os.path.exists(self.config.data_path):
            raise FileNotFoundError(f"Input file not found: {self.config.data_path}")
        return pd.read_csv(self.config.data_path, parse_dates=['Month'], index_col='Month')

    def build_model(self):
        df = self.load_data()
        df.columns = ['passengers']

        # Split the data
        train = df[:-12]
        test = df[-12:]

        # ========== Auto ARIMA ==========
        auto_arima_model = auto_arima(
            train,
            start_p=0, start_q=0,
            max_p=3, max_q=3,
            seasonal=True,
            m=12,
            d=1, D=1,
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True
        )

        # Save ARIMA summary
        with open(os.path.join(self.config.report, 'data_report.txt'), 'a') as f:
            f.write("\n\n--- AUTO ARIMA ---\n")
            f.write(str(auto_arima_model.summary()))

        # Forecast & RMSE
        forecast_auto = auto_arima_model.predict(n_periods=12)
        forecast_auto = pd.Series(forecast_auto, index=test.index)

        rmse_auto = np.sqrt(mean_squared_error(test, forecast_auto))
        with open(os.path.join(self.config.report, 'data_report.txt'), 'a') as f:
            f.write(f"\nAuto ARIMA RMSE: {rmse_auto:.2f}\n")

        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(train, label='Train')
        plt.plot(test, label='Test')
        plt.plot(forecast_auto, label='Auto ARIMA Forecast', color='orange')
        plt.xlabel("Date")
        plt.ylabel("Passengers")
        plt.title("Auto ARIMA Forecast")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.config.report, 'auto_arima_forecast.png'))
        plt.clf()

        # Save ARIMA model
        joblib.dump(auto_arima_model, filename=os.path.join(self.config.model_save_path, 'auto_arima.pkl'))
        logger.info("Auto ARIMA model saved.")

        # ========== Prophet ==========
        df_prophet = df.reset_index().rename(columns={'Month': 'ds', 'passengers': 'y'})
        train_prophet = df_prophet.iloc[:-12]
        test_prophet = df_prophet.iloc[-12:]

        prophet_model = Prophet(weekly_seasonality=False, yearly_seasonality=True)
        prophet_model.fit(train_prophet)

        future = prophet_model.make_future_dataframe(periods=12, freq='MS')
        forecast = prophet_model.predict(future)

        # Save Prophet model
        joblib.dump(prophet_model, os.path.join(self.config.model_save_path, 'prophet.pkl'))
        logger.info("Prophet model saved.")

        # Save forecast
        forecast.to_csv(os.path.join(self.config.report, 'forecast.csv'))

        # Evaluation
        forecast_test = forecast.set_index('ds').loc[test_prophet['ds']]
        forecast_series = forecast_test['yhat']
        rmse_prophet = np.sqrt(mean_squared_error(test_prophet['y'], forecast_series))

        with open(os.path.join(self.config.report, 'data_report.txt'), 'a') as f:
            f.write("\n\n--- PROPHET ---\n")
            f.write(f"PROPHET RMSE: {rmse_prophet:.2f}\n")

        # Forecast plot
        fig = prophet_model.plot(forecast)
        fig.suptitle("Prophet Forecast")
        fig.set_size_inches(10, 5)
        plt.xlabel("Date")
        plt.ylabel("Passengers")
        fig.savefig(os.path.join(self.config.report, 'prophet_forecast.png'))
        plt.clf()

        # Components plot
        fig2 = prophet_model.plot_components(forecast)
        fig2.set_size_inches(10, 8)
        fig2.savefig(os.path.join(self.config.report, 'prophet_components.png'))
        plt.clf()

        logger.info("Forecasts and plots saved.")