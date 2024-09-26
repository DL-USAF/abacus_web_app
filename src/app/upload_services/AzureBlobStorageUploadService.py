import os
import re

from azure.storage.blob import BlobServiceClient
from werkzeug.datastructures import FileStorage

from .BaseUploadService import BaseUploadService
from . import upload_logger


class AzureBlobStorageUploadService(BaseUploadService):
    def __init__(self, datatype):
        upload_logger.info("Upload Pre-Pipeline.")
        super().__init__(datatype)
        self.AZURE_CONNECTION_STRING = os.environ.get("AZURE_CONNECTION_STRING", '')
        self.AZURE_CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME", '')
        self.blob_service_client = BlobServiceClient.from_connection_string(self.AZURE_CONNECTION_STRING)

    def upload(self, file: FileStorage, filename: str):
        blob_client = self.blob_service_client.get_blob_client(container=self.AZURE_CONTAINER_NAME, blob=filename)
        blob_client.upload_blob(file)
        pass

    def verify_config(self):
        if (self.AZURE_CONNECTION_STRING == ''):
            upload_logger.critical("Azure Connection String missing, cannot use Azure upload...")
        if (self.AZURE_CONTAINER_NAME == ''):
            upload_logger.critical("Azure Container Name missing, cannot use Azure upload...")