from django.http import HttpResponse


def index(request):
    return HttpResponse('<a href="/auth/login/">login</a>')

def profile(request):
    return HttpResponse('Profile for %s. <a href="/logout/">logout</a>' % request.user.username)
