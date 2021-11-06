from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import authenticate, login , logout as logout_user
from django.template.loader import render_to_string
from home.forms import AddMarkForm
from django.http import JsonResponse
from .models import Marks, User
# Create your views here.
@login_required
def homeview(request):
    user = request.user
    if user.user_type == 1:
        students = User.objects.filter(user_type=2)
        return render(request,'home.html',{'user':user,'students':students})
    else:
        marks = Marks.objects.filter(student=user).first()
        return render(request,"student-home.html",{'marks':marks})
    

class loginview(generic.TemplateView):
    def get(self,request):
        return render(request,'login.html')
    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        user = authenticate(phone=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            context = {'error': 'The email and password combination is incorrect'}
            return render(request, 'login.html', context)

class RegisterAdmin(generic.TemplateView):
    def get(self,request):
        return render(request,'registeradmin.html')
    def post(self,request):
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        image = request.FILES['image']
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            error = "Two Passwords doesnt match"
            return render(request,'registeradmin.html',{'error':error})
        user = User.objects.create(first_name=fname,last_name=lname,phone=phone,image=image,dob=dob)
        user.set_password(pass1)
        user.user_type = 1
        user.save()
        return redirect('home:login')

class RegisterStudent(generic.TemplateView):
    def get(self,request):
        return render(request,'registerstudent.html')
    def post(self,request):
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        image = request.FILES['image']
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            error = "Two Passwords doesnt match"
            return render(request,'registeradmin.html',{'error':error})
        user = User.objects.create(first_name=fname,last_name=lname,phone=phone,image=image,dob=dob)
        user.set_password(pass1)
        user.user_type = 2
        user.save()
        return redirect('home:login')
    

def logout(request):
    logout_user(request)
    return redirect('home:login')

@login_required
def StudentDetails(request,id):
    student = User.objects.get(id=id)
    return  render(request,'student-details.html',{'student':student})

@login_required
def MarksView(request):
    user = request.user
    if user.user_type == 1:
        marks = Marks.objects.all()
        return render(request,'marks.html',{'marks':marks})
    else:
        return HttpResponse("Not Allowed To View This Page")

@login_required
def AddMarks(request):
    user = request.user
    if user.user_type == 1:
        if request.method == 'POST':
            form = AddMarkForm(request.POST)
            if form.is_valid:
                form.save()
                return redirect('home:marks')
        students = User.objects.filter(user_type=2)
        form = AddMarkForm()
        return render(request,'add-marks.html',{'students':students,'form':form})
    else:
        return HttpResponse("Not Allowed To View This Page")

@login_required
def EditMarks(request,id):
    user = request.user
    if user.user_type == 1:
        if request.method == 'POST':
            mark = Marks.objects.get(id=id)
            form = AddMarkForm(instance=mark,data=request.POST)
            if form.is_valid:
                form.save()
                return redirect('home:marks')
        mark = Marks.objects.get(id=id)
        form = AddMarkForm(instance=mark)
        return render(request,'add-marks.html',{'form':form})
    else:
        return HttpResponse("Not Allowed To View This Page")

def SearchCustomers(request):
    if request.is_ajax():
        search_text = request.GET.get('search')
        print(search_text)
        students = User.objects.filter(user_type=2,first_name__icontains=search_text)
        html = render_to_string('search_student.html',
                                        {'students': students}, request)
        return JsonResponse({'html': html})