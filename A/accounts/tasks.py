from celery import shared_task
from utils import send_otp_code
from datetime import datetime, timedelta
from .models import OtpCode
import pytz


@shared_task
def send_otp_code_task(phone_number, code):
    send_otp_code(phone_number=phone_number, code=code)

@shared_task
def remove_otp_codes():
    expired_time = datetime.now(tz=pytz.timezone('Asia/Dubai')) - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt = expired_time).delete()

