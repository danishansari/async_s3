import asyncio

import aioboto3
import pytest
from aiomoto import *
from moto import mock_s3


@pytest.fixture(scope="module")
def mocker() -> None:
    bucket = "TEST"
    with mock_s3():
        yield asyncio.run(get_cleint(bucket=bucket))


async def get_cleint(bucket: str) -> Any:
    session = aioboto3.Session()
    async with session.client("s3") as client:
        response = await client.create_bucket(
            Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": "us-east-2"}
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        return client
