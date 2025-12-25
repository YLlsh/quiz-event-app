from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from quiz_app.models import *
import json

from django.contrib import messages
# Create your views here.
def home(request):

    return render(request,'home.html')

def quiz_list(request):
    quiz_list = Quiz.objects.all()

    return render(request,'quiz_list.html',{'quiz_list':quiz_list})

def question(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    questions = Question.objects.filter(quiz=quiz).prefetch_related('answer_set')

    # Convert queryset to a list of dictionaries for JS
    question_list = []
    for q in questions:
        options = [(a.text ,a.id) for a in q.answer_set.all().order_by('?')[:4]]
        # correct_index = None
        # for idx, a in enumerate(q.answer_set.all()):
        #     if a.is_correct:
        #         correct_index = idx
        #         break

        question_list.append({
            "id": q.id,
            "question": q.text,
            "options": options,

            # "answer": correct_index
        })


    context = {
        "quiz_data": json.dumps(question_list)  # pass as JSON string
    }

    return render(request, 'questions.html', context)

def score(request):
    if request.method == 'POST':
        # q_id = request.POST.getlist('q_id[]')
        option = request.POST.getlist('answers[]')

        # print(q_id)
        print(option)

    return render(request,'score.html')


def log_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password =password)

        if user is not None:
            login(request, user)
            return redirect('admin_dash')
            messages.error(request,'matched')

        else:
            messages.error(request,'username or password not match')
            return redirect('login')

    return render(request,'login.html')


def log_out(request):
    logout(request)

    return redirect('login')


def admin_dash(request):
    quiz_data = Quiz.objects.all()

    context = {
        'quiz_data':  quiz_data
    }

    return render(request,'admin_dash.html',context)

def add_quiz(request):
    if request.method == 'POST':
        quiz_name = request.POST.get('quiz_name')
        description = request.POST.get('description')

        Quiz.objects.create(
            title  = quiz_name,
            description  = description,
        )
        messages.success(request, 'Quiz added successfully')
        return redirect('admin_dash')

    return render(request,'admin_dash.html')

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

