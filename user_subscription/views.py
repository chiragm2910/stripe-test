from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class HomeView(View):
    """
    This view is to display the home page
    """

    def get(self, request, *args, **kwargs):

        return render(request, "user_subscription/base.html")
