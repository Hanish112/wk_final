from django.urls import path
from panel.views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
]
