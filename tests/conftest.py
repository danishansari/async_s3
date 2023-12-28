import pytest
import aioboto3
import asyncio
from moto import mock_s3

from aiomoto import *


@pytest.fixture(scope="module")
def mocker():
    bucket = "TEST"
    with mock_s3():
        yield asyncio.run(get_cleint(bucket=bucket))


async def get_cleint(bucket):
    session = aioboto3.Session()
    async with session.client("s3") as client:
        response = await client.create_bucket(
            Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": "us-east-2"}
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        return client
