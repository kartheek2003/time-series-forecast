from src.time_series.logger import logger
from src.time_series.pipeline.stage01_data_ingestion import DataIngestionPipeline

STAGE_NAME = "DATA INGESTION"

try :
    logger.info(f">>>>{STAGE_NAME} started<<<<")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(f">>>>{STAGE_NAME} completed<<<<")
except Exception as e:
    raise e