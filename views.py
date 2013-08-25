from django.http import HttpResponse, HttpResponseRedirect
from models import Course, UserProfile, Assignment
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import csv, re


def Register(request):
    return HttpResponse("Nice")
def About(request):
    return HttpResponse("Good")
def Generator(request):
    allofem = Assignment.objects.all()
    for a in allofem:
        a.delete()
    pref = UserProfile.objects.all()
    opt_dict = {}
    for stu in pref:
        opt_dict[stu]= [stu.option1, stu.option2, stu.option3, stu.option4, stu.option5]
    courses = Course.objects.all()
    results = {}
    caps = {}
    for i in courses:
        caps[i.name]= i.max_cap
    for i in courses:
        results[i.name]= []
    for stu in pref:
        print stu.user.username
        for i in range(5):
            if opt_dict[stu][i] != "" and len(results[opt_dict[stu][i]]) < caps[opt_dict[stu][i]] and stu.user not in results[opt_dict[stu][i]]:
                   results[opt_dict[stu][i]].append(stu.user)
            else:
                continue
    for i in results.keys():
        for j in results[i]:
            assignment = Assignment()
            assignment.user = j
            assignment.class_name = i
            print j, i
            assignment.save()
    return HttpResponse("Hello world")

def add_user(content):
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
    form = UploadFileForm(request.POST, request.FILES)
    f = request.FILES['file']
    add_user(f.read())
    return HttpResponseRedirect(reverse('teacher'))
def student(request):
    showed = []
    l = Course.objects.all()
    return render(request, 'student.html', {'courses':l, 'labels':['First', 'Second', 'Third', 'Fourth', 'Fifth']})

def preferences(request):
    user = request.user
    uinfo = UserProfile.objects.get(user_id=user.id)
    uinfo.option1 = request.POST['First']
    uinfo.option2 = request.POST['Second']
    uinfo.option3 = request.POST['Third']
    uinfo.option4 = request.POST['Fourth']
    uinfo.option5 = request.POST['Fifth']
    uinfo.save()
    return HttpResponseRedirect(reverse('student'))

def deleted(request):
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
    return render(request, 'index.html', {})
    
def logggggin(request):
    username = request.POST['username']
    password = request.POST['password']
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
        messages.add_message(request, messages.ERROR, 'Your username or password is invalid')
        return HttpResponseRedirect(reverse('home'))
   
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

    
