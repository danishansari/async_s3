
import aioboto3
import asyncio


@fixture(scope="module")
def mocker():
    bucket = "TEST"
    yield asyncio.run(get_cleint(bucket=bucket))

async def get_cleint(bucket):
    session = aioboto3.session()
    with session.client("s3") as client:
        response = await client.create_bucket()

        return client