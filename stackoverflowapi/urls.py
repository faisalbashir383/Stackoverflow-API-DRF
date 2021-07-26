from django.urls import path,include
from . import views
from .views import QuestionAPI
from rest_framework import routers


router = routers.DefaultRouter()
router.register('questions',QuestionAPI)

urlpatterns = [
    
      path('',views.index,name="index"),
      path('',include(router.urls)),
      path('latest',views.latest_questions,name='latest')
    ]
