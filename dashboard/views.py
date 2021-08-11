from typing import Text
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests, wikipedia
from googletrans import Translator
from django.conf import settings
from django.core.mail import send_mail
import warnings

warnings.catch_warnings()

warnings.simplefilter("ignore")
# Create your views here.

def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(request,"Notes Added Successfully.")
            form = NotesForm()
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    return render(request,'dashboard/notes.html',{'notes':notes,'form':form})

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    messages.success(request,"Note Deleted Successfully.")
    return redirect('notes')

class notesDetailView(generic.DetailView):
    model = Notes

@login_required
def update_note(request,pk=None):
    if request.method == 'POST':
        note = Notes.objects.get(id=pk)
        form = NotesForm(request.POST,instance=note)
        if form.is_valid():
            form.save()
            messages.success(request,"Note Updated Successfully.")
            return redirect('notes')
    else:
        note = Notes.objects.get(id=pk)
        form = NotesForm(instance=note)
    return render(request,'dashboard/updatenote.html', {'form':form})

@login_required
def homework(request):

    if request.method=='POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finish']
                if finished == 'on':
                    finished = True
                else:
                    finished= False
            except:
                finished=False
            
            homeworks=Homework(
                                user=request.user, 
                                subject=request.POST['subject'], 
                                title=request.POST['title'], 
                                description= request.POST['description'], 
                                due=request.POST['due'], 
                                is_finish = finished
                            )
            homeworks.save()
            messages.success(request, 'Homework Added Successfully.')
            form = HomeworkForm()
    else:
        form = HomeworkForm()

    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    
    return render(request,'dashboard/homework.html',{'hw':homework,'hwdone':homework_done,'form':form})

@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finish == True:
        homework.is_finish = False
    else:
        homework.is_finish = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    messages.success(request, 'Homework Deleted Successfully.')
    return redirect('homework')


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i["descriptionSnippet"]:
                    desc = desc + j['text']

            result_dict['description'] = desc
            result_list.append(result_dict)
        return render(request,'dashboard/youtube.html',{'form':form, 'results':result_list})        
    else:
        form = DashboardForm()
    return render(request,'dashboard/youtube.html',{'form':form})

@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finish']
                if finished == 'on':
                    finished = True
                else:
                    finished= False
            except:
                finished=False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finish = finished
            )
            todos.save()
            messages.success(request, 'Todo Added Successfully.')
            form = TodoForm()

    else:
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False

    return render(request,'dashboard/todo.html',{'todo':todo,'tddone':todo_done ,'form':form})

@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finish == True:
        todo.is_finish = False
    else:
        todo.is_finish = True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    messages.success(request, 'Todo Deleted Successfully.')
    return redirect('todo')

@login_required
def edit_todo(request,pk=None):
    if request.method == 'POST':
        todo = Todo.objects.get(id=pk)
        form = TodoForm(request.POST,instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo Updated Successfully.')
            return redirect('todo')
    else:
        todo = Todo.objects.get(id=pk)
        form = TodoForm(instance=todo)
    return render(request,'dashboard/edittodo.html', {'form':form})

def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
        return render(request,'dashboard/books.html',{'form':form, 'results':result_list})        
    else:
        form = DashboardForm()
    return render(request,'dashboard/books.html', {'form':form})


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = { 'form':form,
                        'input':text,   
                        'phonetics':phonetics, 
                        'audio':audio, 
                        'definition':definition,
                        'example':example,
                        'synonyms':synonyms,
                    }                                                    
        except:
            context = { 'form':form,
                        'input':'',
                    }                 
        return render(request,'dashboard/dictionary.html',context)                                   
    else:
        form = DashboardForm()    
    return render(request,'dashboard/dictionary.html',{'form':form}) 


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        try:
            search = wikipedia.page(text)
            context = {
                'form':form,
                'title':search.title,
                'link':search.url,
                'details':search.summary
            }

        except wikipedia.exceptions.DisambiguationError as e:
            context = {
                'form':form,
                'option':e.options
            }
            

        except wikipedia.exceptions.PageError as e:
            context = {
                'form':form,
                'option':e
            }
        
        except wikipedia.exceptions.WikipediaException as e:
            context = {
                'form':form,
                'option':e
            }

        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
    return render(request,'dashboard/wiki.html',{'form':form})

def translate(request):
    if request.method == 'POST':
        text = request.POST['text']
        lang = request.POST['lang']
        translator = Translator()
        dt = translator.detect(text)
        dt2 = dt.lang
        translated = translator.translate(text,lang)
        tr = translated.text
        form = TranslateForm()
        return render(request,'dashboard/translate.html',{'text':text,'translated':tr, 'lang1':lang,'lang2':dt2,'form':form})

    else:
        form = TranslateForm()

    return render(request,'dashboard/translate.html',{'form':form})

@login_required
def profile(request):
    homework = Homework.objects.filter(is_finish = False, user=request.user)
    todo = Todo.objects.filter(is_finish = False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False

    return render(request,'dashboard/profile.html',{'homework':homework,'homework_done':homework_done,'todo':todo,'todo_done':todo_done})


def contact(request):
    if request.method =="POST":
        name= request.POST.get('name','')
        email= request.POST.get('email','')
        contact= request.POST.get('contact','')
        feedback= request.POST.get('feedback','')
        Contact(name=name, email=email, contact=contact, feedback=feedback).save()
        subject = 'Hello ' + name + ' from EduTekBiz.com!'
        message = 'Your Responce: '+feedback+'\nStay Connected. We would love to hear you!'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email, ]
        send_mail(subject, message, email_from, email_to)
        messages.success(request,'Your Feedback is Submitted Successfully and you will get a mail.')
        return redirect("home")

    return render(request, 'dashboard/home.html')