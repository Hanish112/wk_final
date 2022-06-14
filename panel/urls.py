from django.urls import path
from panel.views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('create_table/', create_table, name='create_table'),
]
