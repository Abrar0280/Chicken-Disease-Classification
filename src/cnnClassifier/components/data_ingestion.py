import os
import urllib.request as request
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
import certifi
from cnnClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path

os.environ['SSL_CERT_FILE'] = certifi.where()

import ssl
import urllib.request

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            try:
                with urllib.request.urlopen(self.config.source_URL, context=self.ssl_context) as response:
                    with open(self.config.local_data_file, 'wb') as out_file:
                        data = response.read()
                        out_file.write(data)
                logger.info(f"{self.config.local_data_file} downloaded!")
            except Exception as e:
                logger.error(f"Failed to download file: {e}")
        else:
            file_size = os.path.getsize(self.config.local_data_file)
            logger.info(f"File already exists of size: {file_size} bytes")
    
    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory.
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        try:
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
            logger.info(f"Extracted files to {unzip_path}")
        except zipfile.BadZipFile as e:
            logger.error(f"Failed to extract zip file: {e}")