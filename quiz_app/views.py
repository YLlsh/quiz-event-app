from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from quiz_app.models import *
import json
from django.contrib import messages
from django.utils import timezone
# Create your views here.

@login_required(login_url='login')
def home(request):
    quiz_history = UserSubmission.objects.filter(user_name = request.user)


    return render(request,'home.html',{'quiz_history':quiz_history})


@login_required(login_url='login')
def event(request):
    event_data = Event.objects.filter(date__gte = timezone.now())
    return render(request,'event.html',{'event_data':event_data})


@login_required(login_url='login')
def quiz_list(request):
    quiz_list = Quiz.objects.all()

    return render(request,'quiz_list.html',{'quiz_list':quiz_list})

# ======== questions as per quiz ==========
@login_required(login_url='login')
def question(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('answer_set').order_by('?')[:10]#its get max 10 question in unorder

    # this convert queryset to a list of dictionarie for js
    question_list = []
    for q in questions:
        options = [(a.text ,a.id) for a in q.answer_set.all().order_by('?')] 
   
        question_list.append({
            "id": q.id,
            "question": q.text,
            "options": options,
        })

    context = {# pass as JSON string
        "quiz_data": json.dumps(question_list),
        "quiz_id":quiz.id,  
    }

    return render(request, 'questions.html', context)


# ========= display score ========
@login_required(login_url='login')
def score(request,quiz_id):
    score_count =  request.session.get('score_count',0)
    out_off =  request.session.get('out_off',0)
    if request.method == 'POST':

        option = request.POST.getlist('answers[]')        
       
        True_answer = Answer.objects.filter(
            question__quiz = quiz_id,
            is_correct = True
        )

        answer_list = [] 
        for i in True_answer:
            a = f'{i.question_id}:{i.id}'
            answer_list.append(a)

        # print(answer_list)
        # print()
        # print(option)

        score_count = 0 
        quiz_data =  Quiz.objects.get(id = quiz_id)
        for ans in option:
            q , a = ans.split(':') 
            # split question and answer

            question_data = Question.objects.get(id = int(q))
            ans_data = Answer.objects.get(id = int(a))

            if ans in answer_list:

                score_count += 1
                UserAnswer.objects.create(
                    user = request.user,
                    submission = quiz_data,
                    question = question_data,
                    answer = ans_data.text,
                    is_correct = True
                )
            else:
                UserAnswer.objects.create(
                    user = request.user,
                    submission = quiz_data,
                    question = question_data,
                    answer = ans_data.text,
                    #is_correct if False by default
                )

        
        print(score_count)
        out_off = len(option)

        if option:
            store_score(request, quiz_id , score_count)

        request.session['score_count'] = score_count
        request.session['out_off']  = out_off

    context = {
        'score_count':score_count,
        'out_off':out_off,
        'quiz_id':quiz_id
    }
    return render(request,'score.html',context)


#======== function for store user submision=========
def store_score(request, quiz_id , score):
    quiz_data = Quiz.objects.get(id = quiz_id)
    UserSubmission.objects.create(
        quiz = quiz_data,
        user_name = request.user,
        score = score,
    )
    pass

# ==================FUNCATION FOR AUTHENTICATIONA ===================

# ======for sign up======
def sign_up(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # ===user validation===
        if User.objects.filter(username=username).exists():
            messages.success(request,'Username already exist')
            return redirect('login')
        
        # ==password confirmation==
        if password1 != password2:
            messages.success(request,'Password Not Match')
            return redirect('login')
        else:
            u = User.objects.create(username= username, first_name=full_name)
            u.set_password(password1)
            u.save()
            messages.success(request,'Sign up successfully')
            return redirect('login')
    
    return render(request,'login.html')


# ======fo log in======
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password =password)

        if user is not None:
            login(request, user)
            # ===quiz admin login==
            if user.is_staff:
                request.session.set_expiry(900) # its made log out after 15 minutes
                messages.success(request,'Login successfully')
                return redirect('admin_dash')
            else:
                if User.objects.filter(username = username).exists():
                    request.session.set_expiry(900) # its made log out after 15 minutes
                    messages.success(request,'Login successfully')
                    return redirect('home')

        else:
            messages.error(request,'username or password not match')
            return redirect('login')

    return render(request,'login.html')

# ====for log out====
def log_out(request):
    logout(request)

    return redirect('login')

# ======admin dashboard======
@staff_member_required(login_url='login')
def admin_dash(request):
    quiz_data = Quiz.objects.all()
    question_data = Question.objects.all()
    event_data = Event.objects.all()
    quiz_history = UserSubmission.objects.all()
    

    context = {
        'quiz_data':  quiz_data,
        'question_data':question_data,
        'event_data':event_data,
        'quiz_history':quiz_history
    }

    return render(request,'admin_dash.html',context)


# ================fuction for add quiz=================
@staff_member_required(login_url='login')
def add_quiz(request):
    if request.method == 'POST':
        quiz_name = request.POST.get('quiz_name')
        description = request.POST.get('description')

        if Quiz.objects.filter(title__contains = quiz_name).exists():
            messages.success(request, f'This {quiz_name} Quiz Already exist')
            return redirect('admin_dash')

        Quiz.objects.create(
            title  = quiz_name,
            description  = description,
        )
        messages.success(request, 'Quiz added successfully')
        return redirect('admin_dash')

    return render(request,'admin_dash.html')


# ================fuction for add Question=================
@staff_member_required(login_url='login')
def add_question(request):
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')
        question = request.POST.get('question')
        q_type = request.POST.get('q_type')

        quiz_instance = Quiz.objects.get(id = quiz_id)
        q = Question.objects.create(
            quiz = quiz_instance,
            text = question,
            question_type = q_type
        )

        correct_answer = request.POST.getlist('correct_answer[]')
        answers = request.POST.getlist('answers[]')
        for i in range(len(answers)):
            print(correct_answer)
            print(answers)

            ans = False
            if correct_answer[i] == '1':
                ans = True
            
            Answer.objects.create(
                question = q,
                text = answers[i],
                is_correct = ans,
            )

        messages.success(request, 'Question added successfully')
        return redirect('admin_dash')

    return render(request,'admin_dash.html')

# ================fuction for add event=================
@staff_member_required(login_url='login')
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')

        Event.objects.create(
            title = title,
            description = description,
            date = date,
            location = location,
        )
        messages.success(request, 'Event added successfully')
        return redirect('admin_dash')

    return render(request,'admin_dash.html')


# =============function for delete quiz=================
def delete_quiz(request,id):
    quiz = get_object_or_404(Quiz, id=id)

    quiz.delete()
    messages.error(request,'Quiz is Delete successfully')
    return redirect('admin_dash')

# =============function for delete Question=================
def delete_question(request,id):
    question = get_object_or_404(Question, id=id)

    question.delete()
    messages.error(request,'Question is Delete successfully')
    return redirect('admin_dash')

# =============function for delete Event=================
def delete_event(request,id):
    event = get_object_or_404(Event, id=id)

    event.delete()
    messages.error(request,'Event is Delete successfully')
    return redirect('admin_dash')