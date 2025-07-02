from dataclasses import dataclass
from pathlib import Path
@dataclass
class DataIngestionconfig:
  root_dir : Path
  source_url : str
  local_data_file : Path

@dataclass
class EDA :
    data_path : Path
    report_path : Path
    data_output : Path