import asyncio

import aioboto3
import pytest
from aiomoto import *
from moto import mock_s3


@pytest.fixture(scope="module")
def mocker() -> None:
    """Function to mock s3"""
    bucket = "TEST"
    with mock_s3():
        yield asyncio.run(get_client(bucket=bucket))


async def get_client(bucket: str) -> Any:
    """Function to get async-client"""
    session = aioboto3.Session()
    async with session.client("s3") as client:
        response = await client.create_bucket(
            Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": "us-east-2"}
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        return client
