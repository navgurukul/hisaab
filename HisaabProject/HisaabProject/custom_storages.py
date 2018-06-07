# # custom_storages.py
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import settings

class MediaStorage(S3Boto3Storage):
    location = settings.production.MEDIAFILES_LOCATION
    file_overwrite = False
