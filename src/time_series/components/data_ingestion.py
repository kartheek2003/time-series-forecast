import os
import urllib.request 
import zipfile
from src.time_series.logger import logger
import requests
from src.time_series.entity.config_entity import DataIngestionconfig



class DataIngestionComponent:
    def __init__(self,config:DataIngestionconfig):
        self.config = config

    def download_file(self):
        url=self.config.source_url
        output_path=self.config.local_data_file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info(f"Starting download from {self.config.source_url}...")
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            print(f"File successfully downloaded to: {output_path}")
        except Exception as e:
            print(f"Download failed: {e}")
        return self.config.local_data_file