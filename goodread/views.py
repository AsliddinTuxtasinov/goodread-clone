from django.shortcuts import HttpResponse


def landingPage(request):
    return HttpResponse(content="Django is working, yahooooo")
