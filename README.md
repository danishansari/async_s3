# AsyncS3
S3 access using async apis (aioboto3)


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
