from django.contrib import admin
from django.urls import path
from . import views
# app_name = 'base'
from .views import ClassClinic

urlpatterns = [
    path('clinic/<uuid:clinic_id>', views.view_review, name='viewreview'),
    path('', views.index, name='home'),
    path('comment', views.save_comment, name='comment'),
    path('reply', views.save_reply, name='reply'),
    path('add-clinic', ClassClinic.as_view(), name='add-clinic'),

]