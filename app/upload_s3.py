import os

import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

client = boto3.client(
    service_name='s3',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


def s3_client():
    """
        Function: get s3 client
         Purpose: get s3 client
        :returns: s3
    """
    session = boto3.session.Session()
    client = session.client('s3')
    """ :type : pyboto3.s3 """
    return client


def upload_file_s3(filename, key, bucket_name):
    s3.Bucket(bucket_name).upload_file(Filename=filename, Key=key)


def upload_file_object_s3(file, bucket_name, acl="public-read"):
    k = client.upload_fileobj(
        file,
        bucket_name,
        file.filename,
        ExtraArgs={
            "ACL": acl,
            "ContentType": file.content_type
        }

    )
    print(k)
    return k


def s3_upload_small_files(inp_file_name, s3_bucket_name, inp_file_key, content_type):
    upload_file_response = client.put_object(Body=inp_file_name,
                                             Bucket=s3_bucket_name,
                                             Key=inp_file_key,
                                             ContentType=content_type
                                             )
    print(f" ** Response - {upload_file_response}")
