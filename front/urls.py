from django.urls import path
from front.views import Index

app_name = 'front'
urlpatterns = [
    path('',Index.as_view(), name = 'index'), 
]
