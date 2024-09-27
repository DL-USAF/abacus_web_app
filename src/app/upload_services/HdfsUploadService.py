import os
import re

from hdfs import Config
from werkzeug.datastructures import FileStorage

from .BaseUploadService import BaseUploadService
from . import upload_logger


class HdfsUploadService(BaseUploadService):
    def __init__(self):
        upload_logger.info("Upload HDFS Pre-Pipeline.")
        super().__init__()
        self.HDFS_PROFILE = os.environ.get("HDFS_PROFILE", '')
        self.hdfs_client = Config().get_client(self.HDFS_PROFILE)
        self.default_folder = "/data"

    def upload(self, file: FileStorage, filename: str, datatype: str):
        upload_logger.debug(self.hdfs_client.list('/data'))
        upload_filename = f"/data/{datatype}/{filename}"
        self.hdfs_client.write(upload_filename, file)

    def verify_config(self):
        if (self.HDFS_PROFILE == ''):
            upload_logger.critical("HDFS Profile is missing, cannot use HDFS upload...")

    def get_list_of_datatypes(self):
        folders_to_ignore = ["accumuloConfigCache", "flagged", "flagging", "loaded"]
        folders = self.hdfs_client.list(self.default_folder)
        return [folder for folder in folders if folder not in folders_to_ignore]