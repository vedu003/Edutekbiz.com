from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Notes)
class NotesModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','description']

@admin.register(Homework)
class HomeworkModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','subject','title','description','due','is_finish']

@admin.register(Todo)
class TodoModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','is_finish']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','contact','feedback']