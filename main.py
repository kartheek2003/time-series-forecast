from src.time_series.logger import logger
from src.time_series.pipeline.stage01_data_ingestion import DataIngestionPipeline
from src.time_series.pipeline.stage02_eda import EDAPipeline
from src.time_series.pipeline.stage03_model_building import ModelBuildingPipeline


STAGE_NAME = "DATA INGESTION"

try :
    logger.info(f">>>>{STAGE_NAME} started<<<<")
    obj = DataIngestionPipeline()
    obj.main()
    logger.info(f">>>>{STAGE_NAME} completed<<<<")
except Exception as e:
    raise e

STAGE_NAME = "EDA"
try :
    logger.info(f'>>>>{STAGE_NAME} STARTED<<<<')
    obj = EDAPipeline()
    obj.main()
    logger.info(f">>>>{STAGE_NAME} COMPLETED<<<<")
except Exception as e:
    raise e

STAGE_NAME = "MODEL BUILDING"
try :
    logger.info(f'>>>>{STAGE_NAME} STARTED<<<<')
    obj = ModelBuildingPipeline()
    obj.main()
    logger.info(f">>>>{STAGE_NAME} COMPLETED<<<<")
except Exception as e:
    raise e
