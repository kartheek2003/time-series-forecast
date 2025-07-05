from src.time_series.entity.config_entity import Prediction

import pandas as pd
import joblib
import os
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
import matplotlib.pyplot as plt
import io
from prophet import Prophet
from pathlib import Path
from flask import send_file

class PredictionComponent:
    def __init__(self,config = Prediction):
        self.config = config

    def prediction_with_auto_arima(self,data:pd.DataFrame , periods : int):
        model = joblib.load(self.config.auto_arima)
        forecast = model.predict(n_periods = periods)

        # Generate future index
        last_date = data.index[-1]
        freq = pd.infer_freq(data.index) or 'MS'
        forecast_index = pd.date_range(start=last_date + pd.tseries.frequencies.to_offset(freq),
                                    periods=periods, freq=freq)
        forecast_series = pd.Series(forecast, index=forecast_index)

        # Plot
        plt.figure(figsize=(10, 5))
        plt.plot(data, label="Historical")
        plt.plot(forecast_series, label="Forecast", color='orange')
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.title("Auto ARIMA Forecast")
        plt.legend()
        plt.grid(True)

        # Save to in-memory buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.clf()

        # Return image as response
        return buf
    


    def prediction_with_prophet(self,data: pd.DataFrame, periods: int):
        # Prepare the data
        df = data.reset_index().rename(columns={'Month': 'ds', 'passengers': 'y'})

        # model
        model = joblib.load(self.config.prophet)
        # Make future dataframe and forecast
        future = model.make_future_dataframe(periods=periods, freq='MS')
        forecast = model.predict(future)

        # Plot forecast
        fig = model.plot(forecast)
        fig.suptitle("Prophet Forecast", fontsize=16)
        plt.xlabel("Date")
        plt.ylabel("Passengers")

        # Save plot to in-memory buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        return buf
            