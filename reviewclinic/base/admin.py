from django.contrib import admin

# Register your models here.
from .models import Clinic, Comment, Reply

admin.site.register(Clinic)
admin.site.register(Comment)
admin.site.register(Reply)
