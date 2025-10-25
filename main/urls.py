from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('analyze/', views.analyze_article, name='analyze'),
]
