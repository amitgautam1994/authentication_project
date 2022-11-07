from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from auth_project import settings

# Create your views here.

def home(request):
    return render(request, 'authentication/index.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "email already exists! Please try some other email.")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 character.")

        if pass1 != pass2:
            messages.error(request, "Password didn't match.")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric.")    

        new_user = User.objects.create_user(username, email, pass1)
        new_user.first_name = fname
        new_user.last_name = lname
        new_user.is_active = False
        new_user.save()

        # welcome email
        subject = "Welcome to my project"
        message = "Hello " + new_user.first_name + "!! \n" + " Welcome to my project. Thanks for visiting my website."
        from_email = settings.EMAIL_HOST_USER
        to_list = [new_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)


        

        messages.success(request, "Your account has been successfully created!")
        return redirect('signin')


    return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname':fname})
        else:
            messages.error(request, "Bad credentials!")
            return redirect('home')

    return render(request, 'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

@csrf_exempt 
def reset_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, "Password didn't match.")

        user = User.objects.get(username=username, email=email)
        user.set_password(pass1)
        user.save()

        messages.success(request, "Your password was successfully changed!")
        return redirect('home')

    return render(request, 'authentication/reset_password.html')


        




