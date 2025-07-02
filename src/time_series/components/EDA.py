import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from src.time_series.entity.config_entity import EDA
import os 
class EDAComponent:
    def __init__(self,config:EDA):
        self.config = config

    def load_data(self):
        if not os.path.exists(self.config.data_path):
            raise FileNotFoundError(f"Input file not found: {self.config.data_path}")
        return pd.read_csv(self.config.data_path,parse_dates=['Month'], index_col='Month')
    def get_eda(self):
        df = self.load_data()
        df.columns = ['passengers']
        with open(os.path.join(self.config.report_path, 'data_report.txt'), 'w') as f:
            f.write("Data Head:\n")
            f.write(df.head().to_string())
            f.write("\n\n Column-wise Count:\n")
            f.write(df.count().to_string())
            f.write("\n\n Total Rows:\n")
            f.write(str(len(df)))

        #time series plot 
        plt.figure(figsize=(10,5))
        plt.plot(df,label = 'monthly passengers')
        plt.xlabel('Date')
        plt.ylabel('Number of Passengers')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.config.report_path,'plot.png'))
        plt.clf()

        #seasonal decompose
        result = seasonal_decompose(df, model='multiplicative')
        fig = result.plot()
        fig.set_size_inches(10, 8)
        plt.tight_layout()
        plt.savefig(os.path.join(self.config.report_path, 'seasonal_decompose.png'))
        plt.clf()

        # save df

        df.to_csv(os.path.join(self.config.data_output,'eda_data.csv'))
        