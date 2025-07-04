from src.time_series.constants import *
from src.time_series.utils.common import create_directories , read_yaml
from src.time_series.entity.config_entity import DataIngestionconfig,EDA,Model,Prediction



class ConfigurationManager:
    def __init__(self,config_file_path=CONFIG_FILE_PATH,params_file_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self)->DataIngestionconfig:
        config = self.config.data_ingestion
        data_ingestion_config = DataIngestionconfig(root_dir= config.root_dir,source_url=config.source_url,local_data_file=config.local_data_file)
        return data_ingestion_config
    def get_eda_config(self)->EDA:
        config = self.config.EDA
        create_directories([config.report_path])
        create_directories([config.data_output])
        eda_config = EDA(data_path= config.data_path,report_path=config.report_path,data_output=config.data_output)
        
        return eda_config
    def get_model_config(self)->Model:
        config = self.config.model
        create_directories([config.report])
        model_config = Model(data_path=config.data_path,report=config.report,model_save_path= config.model_save_path)
        return model_config
    def get_prediction_config(self)-> Prediction:
        config = self.config.prediction
        prediction_config = Prediction(auto_arima= config.auto_arima , prophet= config.prophet)
        return prediction_config 