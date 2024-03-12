from bucket import bucket
from celery import shared_task

# TODO: can be async?
def all_bucket_object_task():
    result = bucket.get_objects()
    return result

@shared_task
def delete_object_task(key):
    bucket.delete_object(key)

@shared_task
def download_object_task(key):
    bucket.download_object(key)

@shared_task
def upload_object_task(file_name,name_in_bucket):
    bucket.upload_object(file_name=file_name,name_in_bucket=name_in_bucket)
