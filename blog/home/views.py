from django.shortcuts import render

# Create your views here.
from django.shortcuts import render , redirect,HttpResponse
from .models import contact,UserOTP
from django.contrib import messages
from blogapp.models import Post
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    return render(request ,'home.html')

def CONTACT(request):
    if request.method == "POST":
        name1 = request.POST['name']
        email1 = request.POST['email']
        phone1 = request.POST['phone']
        content1 = request.POST['content']
        if len(name1) < 2 or len(email1) < 3 or len(phone1) < 10 or len(content1) < 4:
            messages.add_message(request, messages.ERROR, 'Please Fill Again !')
        else:
            Contact = contact(name=name1, email=email1, phone=phone1, content=content1)
            Contact.save()
            messages.success(request, "Your message has been successfully sent..We will soon Contact You!!!")




    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    query = request.GET['search']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts}
    return render(request, 'search.html', params)


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if User.objects.filter(username=username ).exists()==True:
            messages.add_message(request, messages.ERROR, 'User Name already in Use!!!')
            return redirect('home')

        if len(username) < 2 or len(email) < 5 or len(fname) < 2 or len(lname) < 3 or len(pass1)<3 or len(pass2)<3 or pass1!=pass2:
            messages.add_message(request, messages.ERROR, 'Please Fill Again !')
            return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname

        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        usr_otp = random.randint(100000, 999999)
        a = UserOTP(user=myuser, otp=usr_otp)
        a.save()
        mess = f"Hello {myuser.first_name},\nYour OTP is {usr_otp}\nThanks!"

        send_mail(
           "Welcome to READ IT BLOG - Verify Your Email",
           mess,
           settings.EMAIL_HOST_USER,
           [myuser.email],
           fail_silently=False
           )
        messages.success(request, "OTP HAS BEEN SENT ON YOUR REGISTERED EMAIL ID..!!!")
        return render(request, 'verifyotp.html', {'usr': myuser})


    else:
        return HttpResponse("404 - Not found")




def verify_otp(request):
    if request.method=="POST":
        otp = request.POST['otp']
        username = request.POST['usr']

        usr = User.objects.get(username=username)
        if otp:



           if int(otp) == UserOTP.objects.filter(user=usr).last().otp:
               usr.is_active=True
               usr.save()
               messages.success(request, "OTP has been matched, You can LOGIN now!!!")
               return redirect("home")
           else:
               messages.error(request, "OTP does not match .please try again!!")
               return render(request, 'verifyotp.html', { 'usr':usr})

        else:
            return render(request, 'verifyotp.html', {'usr':usr})

def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")




def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')