from abc import ABC, abstractmethod
import importlib
import os
import re

from werkzeug.datastructures import FileStorage

from . import upload_logger


class BaseUploadService(ABC):
    def __init__(self):
        self.EXT_REGEX = os.environ.get("EXT_REGEX", "json$")
        self.encryption_enabled = False
        pass

    def verify(self, filename: str):
        return bool(re.search(self.EXT_REGEX, filename))

    @abstractmethod
    def upload(self, file: FileStorage, filename: str, datatype: str):
        pass

    @abstractmethod
    def verify_config(self):
        pass

    @abstractmethod
    def get_list_of_datatypes(self):
        pass


def load_upload_service() -> BaseUploadService:
    upload_service = os.getenv('UPLOAD_SERVICE', 'Mock')

    try:
        module = importlib.import_module(f'app.upload_services.{upload_service}UploadService')
        upload_service_class = getattr(module, f"{upload_service}UploadService")
        return upload_service_class()
    except (ImportError, AttributeError) as e:
        upload_logger.error(e)
        raise ValueError(f"Unknown upload service class: {upload_service}UploadService")