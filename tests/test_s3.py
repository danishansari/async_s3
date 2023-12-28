import pytest
from srcs.async_s3 import AsyncS3


class TestS3:
    @pytest.mark.asyncio
    async def test_upload(self, mocker, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("test s3")

        client = AsyncS3()
        resp = await client.upload_async(str(p), "s3://TEST/test/test.txt")
        assert resp == str(p)

    @pytest.mark.asyncio
    async def test_download(self, mocker, tmp_path):
        p = tmp_path / "test.txt"

        client = AsyncS3()
        resp = await client.download_async("s3://TEST/test/test.txt", str(p))
        assert resp == "s3://TEST/test/test.txt"
