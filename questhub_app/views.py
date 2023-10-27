from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.



def registerpage(request):
    return render(request,'register.html') 


def register_save(request):
    if request.POST:
        username=request.POST['uname']
        password=request.POST['pswd'] 
        email=request.POST['email']   
        
        if Registerprofile.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return redirect('registerpage') 
        elif Registerprofile.objects.filter(email=email).exists():
            messages.info(request,'Email id already exists')
            return redirect('registerpage')
        else :
            register=Registerprofile(username=username,password=password,email=email,)
            register.save()
            messages.success(request,'Your account registered successfully')
            return redirect('loginpage')

    else:
        return redirect('registerpage')    
   

def loginpage(request):
    return render(request,'login.html')    

def userlogin(request):
    if request.POST:
        username = request.POST.get('uname', '')  
        password = request.POST.get('pswd', '')  

        try:
            log_details = Registerprofile.objects.get(username=username, password=password)

        except ObjectDoesNotExist:

            messages.error(request, 'No account found')
            return redirect('loginpage')

        if log_details.position == 'User':
            request.session["user_id"] = log_details.id
            if 'user_id' in request.session:
                if request.session.has_key('user_id'):
                    user_id = request.session['user_id']
                else:
                    return redirect('/')

                user_dash = Registerprofile.objects.get(id=user_id)

                if user_dash:
                    messages.success(request, 'Login Successful')
                    
                    return redirect('index')
                else:
                    return redirect('loginpage')

    return redirect('loginpage')

def index(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        
        context={
            'userdata':userdata,
        }

    return render(request, 'index.html', context)


def userlogout(request):
    request.session.pop('user_id', None)
    messages.success(request,'Logout successfully')
    return redirect('loginpage')
