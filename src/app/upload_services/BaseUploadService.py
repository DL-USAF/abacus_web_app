from abc import ABC, abstractmethod
import importlib
import os
import re

from werkzeug.datastructures import FileStorage


class BaseUploadService(ABC):
    def __init__(self, datatype: str):
        self.EXT_REGEX = os.environ.get("EXT_REGEX", "json")
        self.datatype = datatype
        self.encryption_enabled = False
        pass

    def verify(self, filename: str):
        return re.search(self.EXT_REGEX, filename)

    @abstractmethod
    def upload(self, file: FileStorage, filename: str):
        pass

    @abstractmethod
    def verify_config(self):
        pass


def load_upload_service() -> BaseUploadService:
    upload_service = os.getenv('UPLOAD_SERVICE', 'Mock')

    try:
        module = importlib.import_module(f'app.upload_services.{upload_service}UploadService')
        upload_service_class = getattr(module, f"{upload_service}UploadService")
        return upload_service_class("test")
    except (ImportError, AttributeError) as e:
        print(e)
        raise ValueError(f"Unknown authentication service class: {upload_service}UploadService")