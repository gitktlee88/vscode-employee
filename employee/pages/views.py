from django.http import HttpResponse
from django.shortcuts import render
import requests

from .models import BlogPost

# Create your views here.
def home_view(request, *args, **kwargs):
    # print(args, kwargs)
    # print(request.user)
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "home.html", {})

def contact_view(*args, **kwargs):
    #print(args, kwargs)
    return HttpResponse("<h1>Contact Page</h1>")

def about_view(request, *args, **kwargs):
    #print(args, kwargs)
    my_context = {
        "my_text": "This is about us",
        "my_number": 123,
        "my_list": [23, 35, 55, 123, "hello"]
    }
    return render(request, "about.html", my_context)

def pages_list_view(request):
    queryset = BlogPost.objects.all() # list of objects
    context = {
    'object_list': queryset
    }
    return render(request, "list.html", context)



#################################################
# Passing Parameters to an API:
# GitHub Public API
#################################################
# def github_view(request):
#     user = {}
#     if 'username' in request.GET:
#         username = request.GET['username']
#         url = 'https://api.github.com/users/%s' % username
#         response = requests.get(url)
#         user = response.json()
#     return render(request, 'github.html', {'user': user})

def github_view(request):
    print(request.GET)
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username
        response = requests.get(url)
        search_was_successful = (response.status_code == 200)  # 200 = SUCCESS
        search_result = response.json()
        search_result['success'] = search_was_successful
        search_result['rate'] = {
            'limit': response.headers['X-RateLimit-Limit'],
            'remaining': response.headers['X-RateLimit-Remaining'],
        }
    return render(request, 'github.html', {'search_result': search_result})



############################################
# Managing API Keys: Oxford Dictionaries API
############################################
from .forms import DictionaryForm

def oxford_view(request):
    # print(request)
    # <WSGIRequest: GET '/pages/oxford/?word=heedless'>

    # print(request.GET)
    # <QueryDict: {'word': ['heedless']}>

    search_result = {}
    if 'word' in request.GET:
        form = DictionaryForm(request.GET)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            search_result = form.search()
    else:
        form = DictionaryForm()
    return render(request, 'oxford.html', {'form': form, 'search_result': search_result})


############################################
# Sending email:
############################################
from django.core.mail import send_mail
from .forms import ContactForm
def email_view(request):
    search_result = {}
    form = ContactForm(request.GET)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender = form.cleaned_data['sender']
        cc_myself = form.cleaned_data['cc_myself']

        recipients = ['kyungtak.lee@gmail.com']
        if cc_myself:
            recipients.append(sender)
        try:
            send_mail(subject, message, sender, recipients)
        except Exception as e:
            print(e)
        return HttpResponse('/thanks/')
    else:
        # return HttpResponse('/thanks/')
        return render(request, 'email.html',{'form': form, 'search_result': search_result})
