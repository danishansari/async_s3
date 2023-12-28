
from typing import Callable
from unittest.mock import MagicMock

import aiobotocore.awsrequest
import aiobotocore.endpoint
import aiohttp
import aiohttp.client_reqrep
import aiohttp.typedefs
import botocore.awsrequest
import botocore.model
import pytest

"""
Reference: Patch aiobotocore to work with moto
See https://github.com/aio-libs/aiobotocore/issues/755
"""


class MockAWSResponse(aiobotocore.awsrequest.AioAWSResponse):
    def __init__(self, response: botocore.awsrequest.AWSResponse):
        self._moto_response = response
        self.status_code = response.status_code
        self.raw = MockHttpClientResponse(response)

    # adapt async methods to use moto's response
    async def _content_prop(self) -> bytes:
        return self._moto_response.content

    async def _text_prop(self) -> str:
        return self._moto_response.text


class MockHttpClientResponse(aiohttp.client_reqrep.ClientResponse):
    def __init__(self, response: botocore.awsrequest.AWSResponse):
        async def read(n: int = -1) -> bytes:
            # streaming/range requests. used by s3fs
            if not self.content._eof:
                self.content._eof = True
                return response.content
            return b""

        self.content = MagicMock(aiohttp.StreamReader)
        self.content.read = read
        self.content._eof = False

    @property
    def raw_headers(self) -> aiohttp.typedefs.RawHeaders:
        return ()


@pytest.fixture(scope="session")
def _patch_aiobotocore() -> None:
    def factory(original: Callable) -> Callable:
        def patched_convert_to_response_dict(
            http_response: botocore.awsrequest.AWSResponse, operation_model: botocore.model.OperationModel
        ):
            return original(MockAWSResponse(http_response), operation_model)

        return patched_convert_to_response_dict

    aiobotocore.endpoint.convert_to_response_dict = factory(aiobotocore.endpoint.convert_to_response_dict)