from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from geeksforgeeks import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_text
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth import authenticate, login,logout
from . tokens import generate_token
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Photo
from .forms import PhotoForm


# from authentication.functions.functions import handle_uploaded_file  
# from authentication.forms import StudentForm  


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']       
        Date_Of_Birth=request.POST['Date_Of_Birth']
        country=request.POST['country']
        try:
           gender=request.POST['gender']
        except:
            messages.error(request, "Select any one gender")
            return render(request, 'authentication/signup.html',{'email':email, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})
        
        try:
            image = request.FILES['image']
        except:
            messages.error(request, "Select file")
            return render(request, 'authentication/signup.html',{'email':email, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})   
        try:
            Profession=request.POST['Profession']
        except:
            messages.error(request, "Select any one profession")
            return render(request, 'authentication/signup.html',{'email':email, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})
        
        
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return render(request, 'authentication/signup.html',{'email':email, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})
            # return redirect('signup')
            # we are also uper dictionary add {username=username},we are not use because error throw in username,
         
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return render(request, 'authentication/signup.html',{'username':username, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})
            # return redirect('signup')
            # we are also uper dictionary add {email=email},we are not use because error throw in email,
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return render(request, 'authentication/signup.html',{'email':email, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})
            # return redirect('signup')
            # we are also uper dictionary add {username=username},we are not use because error throw in username,
            
        if pass1 != pass2:
            messages.error(request, " Confirm Passwords didn't matched!!")
            return render(request, 'authentication/signup.html',{'username':username,'email':email, "pass1":pass1, 'fname':fname, 'lname':lname})
            # return redirect('signup')
            # we are also uper dictionary add {pass2},we are not use because error throw in pass2,
            
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return render(request, 'authentication/signup.html',{'email':email, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})
            # return redirect('signup')
             # we are also uper dictionary add {username=username},we are not use because error throw in username,
        # if not  Profession:
        #     messages.error(request, "Profession must be !")
        #     return render(request, 'authentication/signup.html')
        if not Profession:
            messages.error(request, "Select any one profession")
            return render(request, 'authentication/signup.html',{'email':email, "pass1":pass1, 'pass2':pass2, 'fname':fname, 'lname':lname})
             

    
        
         
                                     
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = True
        # myuser.gender=gender
        myuser.Date_Of_Birth= Date_Of_Birth
        myuser.country=country
        myuser.Profession=Profession       
        myuser.image = image
        # myuser.is_active = True
        # myuser.set_password(pass1)
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to my website- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to my website!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address.\n\nThanking You\nVadadoriya chintan"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ my website - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
        print('myuser',myuser)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        print('user',username,pass1)
        
        # user = authenticate(username=username, password=pass1)
        # print('user',user)
                
        try:
            u = User.objects.get(username__exact=username)            
        except User.ObjectDoesNotExist:
            messages.error(request, "incoreect username!!")
            return redirect('signin')
             
        # u = User.objects.get(username__exact=username)
        if u.check_password(pass1):
            print(u, 'correct password')
       
        
            if u is not None:
                login(request, u)
                fname = u.first_name
                # messages.success(request, "Logged In Sucessfully!!")
                
                return render(request, "authentication/index.html",{"fname":fname})
            else:
                messages.error(request, "Bad Credentials!!")
                return redirect('home')
        else:
            messages.error(request, "incorrect password !!")
            print("INCORRECT")
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

# COOKIE SET 

# def setcookie(request):
#     html = HttpResponse("<h3>Welcome to Django page</h3>")
#     html.set_cookie('django', 'We are setting a cookie')
#     return html

# def updating_cookie(request):
#     html = HttpResponse("We are updating  the cookie which is set before")
#     html.set_cookie('django','Updated Successfully')
#     return html

# def updating_cookie1(request):
#     html = redirect(setcookie)
#     html.set_cookie('django','This is your Updated Page')
#     return html

# def deleting_cookie(request):
#     html = HttpResponse("Deleting the cookie which is set")
#     html.delete_cookie('django','Updated Successfully')
#     return html

# def showcookie(request):
#     researcher = None  
#     show = request.COOKIES['django']
#     html = "<center> New Page <br>{0}</center>".format(show)       
#     return HttpResponse(html)

# def setcookie1(request):
#     html = HttpResponse("<h1>Welcome to django </h1>")
#     html.set_cookie('django', 'We are setting a cookie', max_age = None)
#     return html

# def showcookie1(request):
#     show = request.COOKIES['django']
#     html = '<center> New page<br>{0}</center>'.format(show)
#     return HttpResponse(html)

def setcookie(request):
    html = HttpResponse("<h1>Welcome to django</h1>")
    if request.COOKIES.get('visits'):
        html.set_cookie('django', 'Welcome Back')
        value = int(request.COOKIES.get('visits'))
        html.set_cookie('visits', value + 1)
    else:
        value = 1
        text = "Welcome for the first time"
        html.set_cookie('visits', value)
        html.set_cookie('django', text)
    return html

def showcookie(request):
    if request.COOKIES.get('visits') is not None:
        value = request.COOKIES.get('visits')
        text = request.COOKIES.get('django')
        html = HttpResponse("<center><h1>{0}<br>You have requested this page {1} times</h1></center>".format(text, value))
        html.set_cookie('visits', int(value) + 1)
        return html
    else:
        return redirect('setcookie')
    
    # SESSION SET
def setsession(request):
    request.session['sname']='chintan'
    request.session['semail']='chintan@gmail.com'
    return HttpResponse('session is set')

def getsession(request):
    studentname = request.session['sname']  
    studentemail = request.session['semail']  
    return HttpResponse(studentname+"     "+studentemail);

# file upload   

# def index(request):  
#     if request.method == 'POST':  
#         student = StudentForm(request.POST, request.FILES)  
#         if student.is_valid():  
#             handle_uploaded_file(request.FILES['file'])  
#             return HttpResponse("File uploaded successfuly")  
#     else:  
#         student = StudentForm()  
#         return render(request,"authentication/index1.html",{'form':student})     


def photo_list(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'authentication/photo_list.html', {'form': form, 'photos': photos})


