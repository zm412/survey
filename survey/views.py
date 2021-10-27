from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from django.forms import MultiWidget, TextInput
from django.http import JsonResponse
from django import forms
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.decorators.http import require_http_methods
import json

from .models import Question, Survey, Survey_instance, Option, Answer

def get_questions():
    question_list = Question.objects.all()
    list = []
    for a in question_list:
        list.append((a.id, a.question))
    return tuple(list)



class Add_survey(forms.ModelForm):

    question_list = forms.MultipleChoiceField(required=False,
                                             widget=forms.SelectMultiple,
                                             choices=get_questions()
                                            )
    class Meta:
        model = Survey
        fields = ['title', 'description']


class Add_question(forms.ModelForm):
    question_type_list = (('single_choice', 'Single choice'),
                          ('multiple_choice', 'Multiple_choice'),
                          ('text_answ', 'Text answer'))

    question_type = forms.MultipleChoiceField(required=False,
                                             widget=forms.SelectMultiple,
                                             choices=question_type_list
                                            )

    class Meta:
        model = Question
        fields = ['question', 'question_type']
        exclude = ['opt1', 'opt2', 'opt3', 'opt4', 'opt5']


def index(request):
    surveys = [ q.serialize() for q in Survey.objects.all() ]

    if request.user.is_authenticated:
        surveys_inst_started = Survey_instance.objects.filter(user = request.user).filter(is_anonymous=False)
        surveys_new= [ q.serialize() for q in Survey.objects.all().exclude(Q(survey_item__user=request.user) & Q(survey_item__is_anonymous=False)) ]
        return render(request, "survey/index.html", {'form': Add_question(),
                                                     'form_survey': Add_survey(),
                                                     'surveys': surveys,
                                                     'surveys_inst_started': surveys_inst_started,
                                                     'surveys_new': surveys_new,
                                                     'questions': Question.objects.all()})
    else:
        return render(request, "survey/login.html")

def start_surv(request, surv_id):
    message = ''
    survey = Survey.objects.get(id=surv_id)
    try:
        survey_inst = Survey_instance.objects.get(survey=survey, user=request.user )
        message = 'this survey instance alredy started'
        print(survey_inst, 'INSTANCE')
    except Survey_instance.DoesNotExist:
        surv_inst = Survey_instance.objects.create(user=request.user, survey=survey,)
        message = 'survey_inst created'
        print(surv_inst, 'INSTANCE')
    print(message, 'messStartSurvey')
    return HttpResponseRedirect(reverse("index"))

def add_interv(request, surv_id):
    print(request.POST, 'lKLJJ')
    message = ''
    survey_inst = Survey_instance.objects.get(survey_id=surv_id, user=request.user )
    survey = Survey.objects.get(id=surv_id)
    for c in request.POST:
        if(c != 'csrfmiddlewaretoken'):
            quest = Question.objects.get(id=c)
            try:
                old_answer = Answer.objects.get(survey_inst=survey_inst, user=request.user, question=quest )
                new_str = ', '.join(request.POST.getlist(c))
                old_answer.answer=new_str
                message = 'answer is changed'
                print(old_answer, 'old_answer')
            except Answer.DoesNotExist:
                new_str = ', '.join(request.POST.getlist(c))
                answer = Answer.objects.create(
                    user=request.user,
                    question=quest,
                    survey_inst=survey_inst,
                    answer= new_str )
                message = 'answer is added'
                print(answer, 'answer')


    print(message, 'adding interv')
    return HttpResponseRedirect(reverse("index"))

def add_opt(request, quest_id):
    message = ''
    if request.method == "POST" and request.user.is_superuser:
        try:
            quest = Question.objects.get(id=quest_id)
            Option.objects.create(question=quest, option= request.POST['new_opt'] )
            message = 'option is added'
        except Question.DoesNotExist:
            message = 'there is no question with this id'
    print(message, 'added opt')
    return HttpResponseRedirect(reverse("index"))


def delete_opt(request, opt_id):
    message = ''
    try:
        option = Option.objects.get(id=opt_id)
        option.delete()
        message = 'option is deleted'
    except Option.DoesNotExist:
        message = 'there is no option with such id'

    print(message, 'messageDelete')
    return HttpResponseRedirect(reverse("index"))


def update_survey(request, surv_id):
    message = ''
    if request.method == "POST" and request.user.is_superuser:
        survey = Survey.objects.get(id=surv_id)
        survey.title = request.POST['title']
        survey.description = request.POST['description']
        survey.save(update_fields=['title', 'description'])
        message = 'question were updated'
    else:
        message =  'Data is not valid'

    print(message, 'mess')
    return HttpResponseRedirect(reverse("index"))



def add_survey(request):

    message = ''
    if request.method == "POST":
        new_surv = Survey(user=request.user)
        add_form = Add_survey(request.POST, instance=new_surv)

        if add_form.is_valid():
            survey = add_form.save()
            surveys_quests = request.POST.getlist('question_list')

            for c in surveys_quests:
                questionI = Question.objects.get(id=c)
                questionI.quest_collection.add(survey)

            survey.save()
            message =  'Survey is saved'
        else:
            message =  'Data is not valid'
    else:
        message =  'Data is not valid'

    print(message, 'messageDelete')
    return HttpResponseRedirect(reverse("index"))

def del_from_list(request, surv_id, quest_id):
    message = ''
    try:
        survey = Survey.objects.get(id=surv_id)
        question = Question.objects.get(id=quest_id)
        question.quest_collection.remove(survey)
        message =  'Question is deleted from list'
    except Survey.DoesNotExist:
        message = 'there is no survey with such id'

    print(message, 'deleteSurvFromList')
    return HttpResponseRedirect(reverse("index"))

def add_on_list(request, surv_id):
    message = ''
    if request.method == "POST":
        try:
            survey = Survey.objects.get(id=surv_id)
            question = Question.objects.get(id=request.POST['question_id'])
            question.quest_collection.add(survey)
            message =  'Question is added to the list'
        except Survey.DoesNotExist:
            message = 'there is no survey with such id'

    print(message, 'addedFromList')
    return HttpResponseRedirect(reverse("index"))



def delete_survey(request, surv_id):
    message = ''
    try:
        survey = Survey.objects.get(id=surv_id)
        survey.delete()
        message =  'Survey is deleted'
    except Question.DoesNotExist:
        message = 'there is no survey with such id'

    print(message, 'deleteSurvMess')
    return HttpResponseRedirect(reverse("index"))

def delete_question(request, quest_id):
    message = ''
    try:
        question = Question.objects.get(id=quest_id)
        question.delete()
        message = 'question is deleted'
    except Question.DoesNotExist:
        message = 'there is no category with such id'

    print(message, 'messageDelete')
    return HttpResponseRedirect(reverse("index"))



def update_question(request, quest_id):
    if request.method == "POST":
        try:
            question = Question.objects.get(id=quest_id)
            update_form = Add_question(request.POST)
            if update_form.is_valid():
                question.question = request.POST['question']
                question.question_type = request.POST['question_type']
                question.save(update_fields=['question', 'question_type'])
                message = 'question is updated'
                return HttpResponseRedirect(reverse("index"))

            else:
                message = 'data is not valid'
        except Question.DoesNotExist:
            message = 'there is no category with such id'
    else:
        message = 'data is not valid'

    print(message, 'messageUpdate')
    return HttpResponseRedirect(reverse("index"))



def add_question(request):
    message = ''
    error = True

    if request.method == "POST":
        listArr = [ request.POST['opt1'],request.POST['opt2'],request.POST['opt3'],request.POST['opt4'],request.POST['opt5']]
        new_quest = Question(user=request.user)
        add_form = Add_question(request.POST, instance=new_quest)

        if add_form.is_valid():
            question = add_form.save()
            question.save()
            question.question_type = request.POST['question_type']
            question.save(update_fields=[ 'question_type'])

            for k in listArr:
                if any(k):
                    opt = Option.objects.create(question=question, option=k)
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "survey/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "survey/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "survey/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "survey/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "survey/register.html")
