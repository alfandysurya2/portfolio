from pathlib import Path
import os

current_dir = os.getcwd()

CONFIG_FILE_PATH = Path(os.path.join(current_dir, 'config/config.yaml'))
PARAMS_FILE_PATH = Path(os.path.join(current_dir, 'params.yaml'))