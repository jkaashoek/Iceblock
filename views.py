from django.http import HttpResponse, HttpResponseRedirect
from models import Course, UserProfile
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import csv, re

def add_user(content):
    # spamreader = csv.reader(content, delimiter=',', quotechar='|')
    rows = content.split('\r')
    for row in rows[1:]:
        row = row.split(',')
        print 'row', row
        username = row[1].lower() + row[0].lower()
        try:
            user = User.objects.get(username = username)
            print user
        except ObjectDoesNotExist:
            user = User.objects.create_user(username)
        user.set_password(row[2])
        user.first_name = row[0]
        user.last_name = row[1]
        admin_bol = row[5].lower()
        if admin_bol == 'admin':
            user.is_staff = True
        else:
            user.is_staff = False
        user.save()
        try:
            uinfo = UserProfile.objects.get(user_id=user.id)
        except ObjectDoesNotExist:
            uinfo = UserProfile()
        uinfo.user = user
        uinfo.school = row[3]
        print uinfo.school
        if re.match("\d+", row[4]):
            uinfo.grade = int(row[4])
        uinfo.save()
        

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

def upload(request):
    print 'LOOOOOOOOK HEEEEERRRREEEEE', request.FILES, request.POST
    form = UploadFileForm(request.POST, request.FILES)
    f = request.FILES['file']
    add_user(f.read())
    return HttpResponseRedirect(reverse('teacher'))
def student(request):
    showed = []
    l = Course.objects.all()
    return render(request, 'student.html', {'courses':l, 'labels':['First', 'Second', 'Third', 'Fourth', 'Fifth']})

def preferences(request):
    print "preferences", request.POST.keys()
    user = request.user
    print "DAD IS A POOOOOOOPP", user
    uinfo = UserProfile.objects.get(user_id=user.id)
    uinfo.option1 = request.POST['First']
    uinfo.option2 = request.POST['Second']
    uinfo.option3 = request.POST['Third']
    uinfo.option4 = request.POST['Fourth']
    uinfo.option5 = request.POST['Fifth']
    uinfo.save()
    return HttpResponseRedirect(reverse('student'))

def deleted(request):
    # delete = the delete buttons id
    ident = ''
    for key in request.POST.keys():
        if request.POST[key] == 'Delete class':
            ident = key
    if ident != "":
        c = Course.objects.get(pk=ident)
        c.delete()
    return HttpResponseRedirect(reverse('teacher'))
    
def teacher(request):
    l = Course.objects.all()
    # for c in l:
    #    print c
    form = UploadFileForm()
    return render(request, 'teacher.html', {'courses':l, 'form':form})

def newClassForm(request):
    return render(request, 'newClassForm.html', {})

def add_class(request):
    name = request.POST['name']
    teacher = request.POST['teacher name']
    availability = request.POST['availability']
    description = request.POST['description']
    max_cap = request.POST['max_cap']
    if request.POST['submit'] == "Done":
        return HttpResponseRedirect(reverse('teacher'))
    else:
        print name, teacher, availability, description, max_cap
        c = Course()
        c.name = name
        c.teacher = teacher
        c.available = availability
        c.max_cap = max_cap
        c.description = description
        c.save()
        return HttpResponseRedirect(reverse('newClassForm'))
    

def home(request):
    # print "home:"
    return render(request, 'index.html', {})
    
def logggggin(request):
    username = request.POST['username']
    password = request.POST['password']
    # print "login", username, password
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            u = User.objects.get(username__exact=username)
            if u.is_staff:
                return HttpResponseRedirect(reverse('teacher'))
            else:
                return HttpResponseRedirect(reverse('student'))
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
       return HttpResponseRedirect(reverse('home'))
   
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

## 1. Login page (documentation at: https://docs.djangoproject.com/en/dev/topics/auth/default/#user-objects)
## 2. Find out how to redirect (look at views part in tutorial)
## 3. Find out how to display error
## 4. Make login page beautius (bootstrap)

## 1. Create users (figure out how to set username as lastFirst)
## 2. Show classes that are only offered for that grade. 6-8 means 6, 7, 8
## if studentuser.grade >= available[0] and studentuser.grade <= available[2]:
##     print
## else:
## 3. Get a list of preferences for user.id
    
