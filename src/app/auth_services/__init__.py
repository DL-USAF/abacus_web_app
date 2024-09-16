import os
from pathlib import Path
from ..utils.create_logger import create_logger


auth_log_file = "logs/auth_logging.log"
if (not Path(auth_log_file).parent.exists()):
    os.makedirs(Path(auth_log_file).parent)

logger = create_logger("abacus_web_app_auth", auth_log_file)