import asyncio
from typing import Any

from srcs.async_s3 import AsyncS3


class TestS3():
    """AsyncS3 test class"""


    def test_upload(self, mocker: Any, tmp_path: Any):
        """test async-s3 upload function"""
        p = tmp_path / "test.txt"
        p.write_text("test s3")
        
        client = AsyncS3()
        resp = client.upload(str(p), "s3://TEST/test/test.txt")
        assert resp == str(p)

        resp = asyncio.run(mocker.head_object(Bucket="TEST", Key="test/test.txt"))
        assert resp["ResponseMetadata"]["HTTPStatusCode"] == 200
        
        
        
    def test_download(self, mocker: Any, tmp_path: Any):
        """test async-s3 upload function"""
        p = tmp_path / "test.txt"

        resp = asyncio.run(mocker.head_object(Bucket="TEST", Key="test/test.txt"))
        assert resp["ResponseMetadata"]["HTTPStatusCode"] == 200

        client = AsyncS3()
        resp = client.download("s3://TEST/test/test.txt", str(p))
        assert resp == "s3://TEST/test/test.txt"
