from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages


class UsernameValidationView(View):
    def post(self, request):

        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({"username_error": "Username must include characters, numbers and special characters"}, status=400)
        
        # if the username already taken/exist in the database
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Username already exist"}, status=409)

        return JsonResponse({"email_valid": True})

class EmailValidationView(View):
    def post(self, request):

        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({"email_error": "Email is invalid"}, status=400)
        
        # if the username already taken/exist in the database
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Email already exist"}, status=409)

        return JsonResponse({"email_valid": True})

class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'authentication/register.html' )

    def post(self, request, *args, **kwargs):

        messages.success(request, 'Registration successfully')
        messages.warning(request, 'Registration successfully, warning')
        messages.error(request, 'Registration successfully error')
        messages.info(request, 'Registration successfully info')

        return render(request, 'authentication/register.html' )
