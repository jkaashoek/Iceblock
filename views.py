from django.http import HttpResponse, HttpResponseRedirect
from models import Course, UserProfile, Assignment
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
import csv, re

def Publish(request):
    print "PUBLISH"
    assignments = Assignment.objects.all()
    with open('publish.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Student', 'Assignment', 'Homeroom'])
        for i in assignments:
            spamwriter.writerow([i.user_id, i.class_name])
    f = open('publish.csv', 'r')
    print "Email is about to run"
    mail = EmailMessage('Final class assignments', 'Your final class assignments are attached', 'justin.kaashoek@gmail.com',
                        ['justin.kaashoek@gmail.com'])
    mail.attach('publish.csv', f.read(), 'text/csv')
    mail.send(fail_silently = False)
    return HttpResponseRedirect(reverse('showassignments')) 
        

def Register(request):
    return HttpResponse("Nice")

def About(request):
    return render(request, 'aboutus.html',{})

def mkkey(classname, grade):
    return classname+" G"+grade

def canassign(classpref, stu, stugrade, caps, results):
    if classpref == '':
        return False
    try:
        if len(results[mkkey(classpref, stugrade)]) < caps[mkkey(classpref,stugrade)] and stu not in results[mkkey(classpref,stugrade)]:
            return True
        else:
            return False
    except KeyError:
        return False
     
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
        caps[mkkey(i.name,i.available)]= i.max_cap
    for i in courses:
        results[mkkey(i.name, i.available)]= []
    for stu in pref:
        for i in range(5):
            if canassign(opt_dict[stu][i], stu.user, str(stu.grade), caps, results):
                results[mkkey(opt_dict[stu][i], str(stu.grade))].append(stu.user)
            else:
                continue
    for i in results.keys():
        for j in results[i]:
            assignment = Assignment()
            assignment.user = j
            assignment.class_name = i
            assignment.save()
    return HttpResponseRedirect(reverse('showassignments')) 

def showassignments(request):
    classassignment = {}
    allassignments = Assignment.objects.all()
    for a in allassignments:
        if a.class_name in classassignment:
            classassignment[a.class_name].append(a.user)
        else:
            classassignment[a.class_name] = [a.user]
    return render(request, 'showassignments.html', {'assignments': classassignment})

def add_user(content):
    rows = content.split('\r')
    for row in rows[1:]:
        row = row.split(',')
        username = row[1].lower() + row[0].lower()
        try:
            user = User.objects.get(username = username)
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
        if re.match("\d+", row[4]):
            uinfo.grade = int(row[4])
        uinfo.save()
        

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def upload(request):
    form = UploadFileForm(request.POST, request.FILES)
    f = request.FILES['file']
    add_user(f.read())
    return HttpResponseRedirect(reverse('teacher'))
def student(request):
    showed = []
    usr = request.user
    Student = UserProfile.objects.get(user_id=usr)
    classes = Course.objects.filter(available=Student.grade)
    return render(request, 'student.html', {'courses':classes, 'labels':['First', 'Second', 'Third', 'Fourth', 'Fifth']})

def preferences(request):
    user = request.user
    uinfo = UserProfile.objects.get(user_id=user.id)
    uinfo.option1 = request.POST['First']
    uinfo.option2 = request.POST['Second']
    uinfo.option3 = request.POST['Third']
    uinfo.option4 = request.POST['Fourth']
    uinfo.option5 = request.POST['Fifth']
    pref_list = [uinfo.option1, uinfo.option2, uinfo.option3, uinfo.option4, uinfo.option5]
    pref_list2 = []
    error=False
    for i in pref_list:
        if i in pref_list2:
            messages.add_message(request, messages.ERROR, 'Your preferences were not submitted. All your preferences must be different')
            error = True
            break
        pref_list2.append(i)
    if error == False:
        uinfo.save()
        messages.add_message(request, messages.SUCCESS, 'Your preferences were successfully sumbitted. Feel free to change your preferences at any time')
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
    c = Course()
    c.name = name
    c.teacher = teacher
    c.available = availability
    c.max_cap = max_cap
    c.description = description
    c.save()
    return HttpResponseRedirect(reverse('teacher'))
    

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

    
