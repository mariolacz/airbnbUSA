import boto3
import os
import yaml

with open("secrets.yaml", "r") as file:
    secrets = yaml.safe_load(file)

client = boto3.client('s3',
                      aws_access_key_id= secrets['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=secrets['AWS_SECRET_ACCESS_KEY']
                      )

bucket_name='projectmcz'
file_name="csv/AB_US_2023.csv"

root_path = os.getcwd()

downloads_dir = os.path.join(root_path, "downloads")
os.makedirs(downloads_dir, exist_ok=True)
download_file_path = os.path.join(downloads_dir, os.path.basename(file_name))

client.download_file(
    Bucket = bucket_name,
    Key = file_name,
    Filename = download_file_path
)

