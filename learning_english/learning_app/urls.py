from django.urls import path

from . import views

app_name = "learning_app"
urlpatterns = [
    path('', views.menu, name="menu"),
    path('word_list/', views.word_list, name="word_list"),
    path('word_list/<int:word_id>/', views.detail, name="detail")
]
