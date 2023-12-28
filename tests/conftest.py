import pytest
import aioboto3
import asyncio


@pytest.fixture(scope="module")
def mocker():
    bucket = "TEST"
    yield asyncio.run(get_cleint(bucket=bucket))

async def get_cleint(bucket):
    session = aioboto3.session()
    with session.client("s3") as client:
        response = await client.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={"LocationConstraints", "us-east-2"}
        )
        assert(response["ResponseMetadata"]["HTTPStatusCode"] == 200)
        return client