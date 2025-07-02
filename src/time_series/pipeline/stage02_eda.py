from src.time_series.config.configuration import ConfigurationManager
from src.time_series.components.EDA import EDAComponent
from src.time_series.logger import logger


class EDAPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        eda_config = config.get_eda_config()
        eda_comp = EDAComponent(config= eda_config)
        eda_comp.get_eda()

STAGE_NAME = "EDA"

if __name__ == "__main__":
    try :
        logger.info(f'>>>>{STAGE_NAME} STARTED<<<<')
        obj = EDAPipeline()
        obj.main()
        logger.info(f">>>>{STAGE_NAME} COMPLETED<<<<")
    except Exception as e:
        raise e