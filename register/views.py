from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.conf import settings
from twilio.rest import Client
import random, json
from .models import Supporter

def register_page(request):
    return render(request, 'register.html')

@csrf_exempt
def send_otp(request):
    data = json.loads(request.body)
    phno = data.get('phno')
    otp = str(random.randint(1000, 9999))
    cache.set(phno, otp, timeout=300)

    # Send OTP using Twilio
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phno
        )
        return JsonResponse({"status": "OTP sent"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt
def verify_and_save(request):
    data = json.loads(request.body)
    otp = data.get('otp')
    cached_otp = cache.get(data.get('phno'))
    if otp == cached_otp:
        supporter = Supporter(
            name=data['name'],
            age=data['age'],
            phno=data['phno'],
            email=data['email'],
            support=data['support']
        )
        supporter.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "invalid OTP"})
