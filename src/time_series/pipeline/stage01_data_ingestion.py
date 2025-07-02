from src.time_series.config.configuration import ConfigurationManager
from src.time_series.components.data_ingestion import DataIngestionComponent
from src.time_series.logger import logger


class DataIngestionPipeline:
    def __init__(self):
        pass
    def main(self):
        config  = ConfigurationManager()
        data_ingestion_configuration = config.get_data_ingestion_config()
        data_ing_comp = DataIngestionComponent(config=data_ingestion_configuration)
        data_ing_comp.download_file()

STAGE_NAME = "DATA INGESTION"

if __name__ == "__main__":
    try :
        logger.info(f">>>>{STAGE_NAME} started<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>{STAGE_NAME} completed<<<<")
    except Exception as e:
        raise e