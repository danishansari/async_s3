from srcs.async_s3 import AsyncS3
import argparse

parser = argparse.ArgumentParser("Async-S3 upload/download app.")
parser.add_argument("-u", "--upload", action="store_true", description="upload files mode")
parser.add_argument("-d", "--download", action="store_true", description="download files mode")
parser.add_argument("-s", "-src", "--source", type="str", description="source files location")
parser.add_argument("-d", "-dst", "--destination", type="str", description="destination files location")


def main():
    args = parser.parse_args()

    s3 = AsyncS3()
    if args.upload:
        s3.upload(args.source, args.destination)
    else:
        s3.download(args.source, args.destination)


if __name__=="__main__":
    main()