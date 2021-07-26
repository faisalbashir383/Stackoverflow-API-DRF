from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from django.utils.decorators import method_decorator
from django.utils.decorators.cache import cache_page
from django.utils.decorators.vary import vary_on_cookie,vary_on_headers
from .models import Question
from .serializer import QuestionSerializer
from bs4 import BeautifulSoup
import requests
import json
from stackoverflowapi.throttling import FaisalRateThrottle 

# Create your views here.


def index(request):
    return HttpResponse('working successfully')
    
    
    
    

class QuestionAPI(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class=QuestionSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    filter_backends = [SearchFilter]
    search_fields = ['question','vote_count','views','tags']

    

def latest_questions(request):
    try:
        res = requests.get('https://stackoverflow.com/questions')
        soup=BeautifulSoup(res.text,'html.parser')
        questions_data = {
            'questions':[]
        }
        questions = soup.select('.question-summary')
        for que in questions:
            q=que.select_one('.question-hyperlink').getText()
            vote_count =que.select_one('.vote-count-post').getText()
            views = que.select_one('.views').attrs['title']
            tags = [i.getText() for i in (que.select('.post-tag'))]
            question = Question()
            question.question = q
            question.vote_count = vote_count
            question.views=views
            question.tags=tags
            question.save()
        return HttpResponse('Data Fetched from stackoverflow')    
    
    except:
        return HttpResponse('Failed')
    