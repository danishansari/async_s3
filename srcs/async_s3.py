import os
import aioboto3
import asyncio

from loguru import logger

from typing import Any

from srcs.utils import S3Url

class AsyncS3:
    """ Class to access aws-s3 bucket to upload and dowanload files
    """

    def __init__(self):
        # create an async s3 session
        self.session = aioboto3.Session()

    def upload(self, local_file_path: str, remote_s3_uri: str) -> str:
        """Function to upload a loacal file to s3-location asynchronously"""
        return asyncio.run(self.upload_async(local_file_path, remote_s3_uri))

    def download(self, remote_s3_uri: str, local_file_path: str) -> str:
        """Function to download a s3-file to a loacal asynchronously"""
        return asyncio.run(self.download_async(remote_s3_uri, local_file_path))
    
    async def upload_async(self, local_file_path: str, remote_s3_uri: str) -> str:
        """Async Function to upload a loacal file to s3-location asynchronously"""
        assert os.path.exists(local_file_path), f"File {local_file_path} not Found!!"

        s3 = S3Url(remote_s3_uri)
        async with self.session.client("s3") as client:
            response = await client.upload_file(
                Bucket = s3.bucket,
                Filename = local_file_path,
                Key = s3.key
            )
        if response["Meta"]["HttpResponse"] == 200:
            logger.info("Upload success!!")
        else:
            logger.error("Upload failed!!")
            local_file_path = "error"
        return local_file_path
    
    async def download_async(self, remote_s3_uri: str, local_file_path: str) -> str:
        """Async Function to download a s3-file to a loacal asynchronously"""
        assert os.path.exists(local_file_path), f"File {local_file_path} not Found!!"

        s3 = S3Url(remote_s3_uri)
        async with self.session.client("s3") as client:
            response = await client.download_file(
                Bucket = s3.bucket,
                Filename = local_file_path,
                Key = s3.key
            )
        if response["Meta"]["HttpResponse"] == 200:
            logger.info("Upload success!!")
        else:
            logger.error("Upload failed!!")
            local_file_path = "error"
        return local_file_path
