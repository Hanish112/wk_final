from django.urls import path
from panel.views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('create_table/', create_table, name='create_table'),
    path('callback/', callback, name='callback')
]
