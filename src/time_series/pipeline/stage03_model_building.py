from src.time_series.config.configuration import ConfigurationManager
from src.time_series.logger import logger
from src.time_series.components.model_building import ModelBuildingComponent

class ModelBuildingPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        model_config = config.get_model_config()
        model_build_comp = ModelBuildingComponent(config= model_config)
        model_build_comp.build_model()
    
STAGE_NAME = "MODEL BUILDING"

if __name__ == "__main__":
    try :
        logger.info(f'>>>>{STAGE_NAME} STARTED<<<<')
        obj = ModelBuildingPipeline()
        obj.main()
        logger.info(f">>>>{STAGE_NAME} COMPLETED<<<<")
    except Exception as e:
        raise e
