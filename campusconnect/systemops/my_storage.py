# systemops/storage_settings.py

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location 		= 'media'
    default_acl 	= 'public-read'
    file_overwrite 	= False
    