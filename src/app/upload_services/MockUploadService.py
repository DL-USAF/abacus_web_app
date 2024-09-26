import os
import re

from azure.storage.blob import BlobServiceClient
from werkzeug.datastructures import FileStorage

from .BaseUploadService import BaseUploadService
from . import upload_logger


class MockUploadService(BaseUploadService):
    def __init__(self, datatype):
        upload_logger.info("Upload Pre-Pipeline.")
        super().__init__(datatype)

    def upload(self, file: FileStorage, filename: str):
        upload_logger.info(f"File to upload: {filename}")
        pass

    def verify_config(self):
        pass