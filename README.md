# AsyncS3 - AWS Asynchronous access 
Wrapper to access aws, using boto3 resources with the aiobotocore async backend 

Provides:
 * Asynchronous s3-access
 * downloading of files from s3-bucket
 * uploading of file to s3-bucket
 * Mock Testing (aws-patched-response)

## Dependencies
 * python-3.11.0

## Installation
```
    pip install -r requirements.txt
```

## Usage
- Upload
```
    from srcs.async_s3 import AsyncS3

    s3 = AsyncS3()
    s3.upload("local/file/path", "s3/location/path")
```
- Download
```
    from srcs.async_s3 import AsyncS3

    s3 = AsyncS3()
    s3.download("s3/location/path", "local/file/path")
```

## Test
```
    python -m pytest
```
