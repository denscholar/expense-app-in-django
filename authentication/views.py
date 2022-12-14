from audioop import reverse
from lib2to3.pgen2 import token
from multiprocessing import context
from urllib import response
from webbrowser import get
from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from .utils import token_generator

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site


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
        return render(request, 'authentication/register.html')

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'field_values': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(
                        request, 'Password should not be less than 6 characteers')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)

                user.is_active = False  # so the user cannot log in before activation

                user.save()  # saves the user in the database

                uidb64 = urlsafe_base64_encode((force_bytes(user.pk)))

                domain = get_current_site(request).domain

                link = reverse('activate', kwargs={
                    'uidb64': uidb64,
                    'token': token_generator.make_token(user)
                })

                activcate_url = 'http://' + domain + link

                email_body = 'Hi, ' + user.username + \
                    'Please use this link to verify your account' + activcate_url
                email_subject = 'Activate your account'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@denscholar.com',
                    [email],
                )

                email.send(fail_silently=False)

                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')
