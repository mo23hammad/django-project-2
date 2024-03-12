from django.conf import settings
import boto3

class Bucket:
    """CDN Bucket Manager

    
    init method creates connection

    NOTE:
        none of these methods are async. use public interface in tasks.py modules instead.
    """
    def __init__(self):
        session = boto3.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket = settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        else:
            return None
    
    def delete_object(self,key):
        self.conn.delete_object(Bucket = settings.AWS_STORAGE_BUCKET_NAME,Key = key)
        return True
    def download_object(self,key):
        with open(settings.AWS_LOCAL_STORAGE + key,'wb') as f:
            self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME,key,f)
        return True
    def upload_object(self,file_name,name_in_bucket):
        self.conn.upload_fileobj(file_name,settings.AWS_STORAGE_BUCKET_NAME,name_in_bucket)
        return True

bucket = Bucket()