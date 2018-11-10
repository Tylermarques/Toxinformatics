from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run_bash', views.run_bash)
]