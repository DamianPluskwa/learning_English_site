from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu, name="menu"),
    path('word_list/', views.word_list, name="word_list")
]
