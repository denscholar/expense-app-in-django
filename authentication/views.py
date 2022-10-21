from django.shortcuts import render
from django.views import View


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'authentication/register.html' )
