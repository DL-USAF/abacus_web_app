import os
import re

from azure.storage.blob import BlobServiceClient
from werkzeug.datastructures import FileStorage

from .BaseUploadService import BaseUploadService
from . import upload_logger


class MockUploadService(BaseUploadService):
    def __init__(self):
        upload_logger.info("Upload Pre-Pipeline.")
        super().__init__()

    def upload(self, file: FileStorage, filename: str, datatype: str):
        upload_logger.info(f"File to upload: {filename} for datatype: {datatype}")
        pass

    def verify_config(self):
        pass

    def get_list_of_datatypes(self):
        return [f"Data {x}" for x in range(5)]