from django.urls import path
from dashboard import views

urlpatterns = [
    path('',views.home, name="home"),

    path('notes/',views.notes, name="notes"),
    path('deletenote/<int:pk>',views.delete_note, name="deletenote"),
    path('updatenote/<int:pk>',views.update_note, name="updatenote"),
    path('notesdetails/<int:pk>',views.notesDetailView.as_view(), name="notedetails"),

    path('homework/',views.homework, name="homework"),
    path('updatehomework/<int:pk>',views.update_homework, name="updatehomework"),
    path('deletehomework/<int:pk>',views.delete_homework, name="deletehomework"),

    path('youtube/',views.youtube, name="youtube"),

    path('todo/',views.todo, name="todo"),
    path('updatetodo/<int:pk>',views.update_todo, name="updatetodo"),
    path('deletetodo/<int:pk>',views.delete_todo, name="deletetodo"),
    path('edittodo/<int:pk>',views.edit_todo, name="edittodo"),

    path('books/',views.books, name="books"),

    path('dictionary/',views.dictionary, name="dictionary"),

    path('wiki/',views.wiki, name="wiki"),

    path('translate/',views.translate, name="translate"),

    path('profile/',views.profile, name="profile"),

    path('contact/', views.contact, name='contact'),
]