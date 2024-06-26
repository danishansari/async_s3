"""
conftest.py - Project Wide Fixtures

ref: https://gist.github.com/giles-betteromics/12e68b88e261402fbe31c2e918ea4168
"""

from typing import Any, Callable
from unittest.mock import MagicMock

import aiobotocore.awsrequest
import aiobotocore.endpoint
import aiohttp
import aiohttp.client_reqrep
import aiohttp.typedefs
import botocore.awsrequest
import botocore.model
import pytest


class MockAWSResponse(aiobotocore.awsrequest.AioAWSResponse):
    """
    Mocked AWS Response.

    https://github.com/aio-libs/aiobotocore/issues/755
    https://gist.github.com/giles-betteromics/12e68b88e261402fbe31c2e918ea4168
    """

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
    """
    Mocked HTTP Response.
    """

    def __init__(self, response: botocore.awsrequest.AWSResponse):
        """
        Mocked Response Init.
        """

        async def read(self: MockHttpClientResponse, n: int = -1) -> bytes:
            return response.content

        self.content = MagicMock(aiohttp.StreamReader)
        self.content.read = read
        self.response = response

    @property
    def raw_headers(self) -> Any:
        """
        Return the headers encoded the way that aiobotocore expects them.
        """
        return {
            k.encode("utf-8"): str(v).encode("utf-8")
            for k, v in self.response.headers.items()
        }.items()


class PatchedAWSResponse:
    """
    Pacthed AWS Response.
    """

    def __init__(self, response: botocore.awsrequest.AWSResponse):
        self._response = response
        self.status_code = response.status_code
        self.raw = response.raw
        self.raw.raw_headers = {}

    @property
    async def content(self):
        return self._response.content


@pytest.fixture(scope="session", autouse=True)
def patch_aiobotocore() -> None:
    """
    Pytest Fixture Supporting S3FS Mocks.
    """

    def factory(original: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
        """
        Response Conversion Factory.
        """

        def patched_convert_to_response_dict(
            http_response: botocore.awsrequest.AWSResponse,
            operation_model: botocore.model.OperationModel,
        ) -> Any:
            return original(MockAWSResponse(http_response), operation_model)

        return patched_convert_to_response_dict

    def factory_2(original: Callable) -> Callable:
        def patched_looks_like_special_case_error(response, **kwargs):
            return original(MockAWSResponse(response), **kwargs)

        return patched_looks_like_special_case_error

    aiobotocore.handlers._looks_like_special_case_error = factory_2(
        aiobotocore.handlers._looks_like_special_case_error
    )

    aiobotocore.endpoint.convert_to_response_dict = factory(
        aiobotocore.endpoint.convert_to_response_dict
    )
