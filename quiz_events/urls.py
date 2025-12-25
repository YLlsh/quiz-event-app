"""
URL configuration for quiz_events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from quiz_app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',home, name="home"),
    path('event/',event,name="event"),
    path('quiz_list/',quiz_list,name="quiz_list"),
    path('question/<int:id>/',question,name="question"),
    path('score/<int:quiz_id>/',score,name="score"),

    path('add_quiz/',add_quiz,name="add_quiz"),
    path('add_question/',add_question,name="add_question"),
    path('add_event/',add_event,name="add_event"),

    path('login/',log_in,name="login"),
    path('admin_dash/',admin_dash,name="admin_dash"),
    path('log_out/',log_out,name="log_out"),


]
