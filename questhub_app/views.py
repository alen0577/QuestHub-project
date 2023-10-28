from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

def userlogout(request):
    request.session.pop('user_id', None)
    messages.success(request,'Logout successfully')
    return redirect('loginpage')


def index(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        questions=Questions.objects.all().order_by('-date','-time')

        context={
            'userdata':userdata,
            'questions':questions,
            'user_id':user_id,
        }

    return render(request, 'index.html', context)

def askquestion(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')

        user=Registerprofile.objects.get(id=user_id)
        if request.POST:
            question=request.POST['question']
            data=Questions(user=user,question=question)
            data.save()
            messages.success(request,'Success')
            return redirect('index')

    else:
        return redirect('/')


def submit_answer(request,pk):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')

        user=Registerprofile.objects.get(id=user_id)
        question=Questions.objects.get(id=pk)

        # Check if the user has already answered this question
        existing_answer = Answer.objects.filter(user=user, question=question)
        if existing_answer.exists():
            messages.info(request,'Already answered..!')
            return redirect('index')

        if request.POST:
            answer_text=request.POST['answer_text']
            data=Answer(answer_text=answer_text,user=user,question=question)
            data.save()
            messages.success(request,'Success')
            return redirect('index')
        
    else:
        return redirect('/')

def view_answers(request,pk):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        question=Questions.objects.get(id=pk)
        answers=Answer.objects.filter(question=question).order_by('-date','-time')
        print(answers)

        context={
            'userdata':userdata,
            'question':question,
            'answers':answers,
            'user_id':user_id,
        }
    return render(request,'answers.html',context)


def like_answer(request, answer_id):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id).id
        if request.method == 'GET' :
            try:
                answer = get_object_or_404(Answer, id=answer_id)

                # Check if the user has already liked this answer to prevent double-liking
                if userdata in answer.likes.all():
                    return JsonResponse({'success': False, 'error': 'You have already liked this answer.'})

                # Add the user to the likes
                answer.likes.add(userdata)

                like_count = answer.like_count()

                return JsonResponse({'success': True, 'like_count': like_count})
            except Answer.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Answer not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})