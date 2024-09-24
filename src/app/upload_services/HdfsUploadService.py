import os
import re

from hdfs import Config
from werkzeug.datastructures import FileStorage

from .BaseUploadService import BaseUploadService
from . import upload_logger


class HdfsUploadService(BaseUploadService):
    def __init__(self, datatype: str):
        upload_logger.info("Upload HDFS Pre-Pipeline.")
        super().__init__(datatype)
        self.HDFS_PROFILE = os.environ.get("HDFS_PROFILE", '')
        self.hdfs_client = Config().get_client(self.HDFS_PROFILE)

    def upload(self, file: FileStorage, filename: str):
        self.hdfs_client.list('/')
        self.hdfs_client.write(filename, file)
        pass

    def verify_config(self):
        if (self.HDFS_PROFILE == ''):
            upload_logger.critical("HDFS Profile is missing, cannot use HDFS upload...")