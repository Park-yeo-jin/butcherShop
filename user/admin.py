from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User

class UserAdmin(ModelAdmin):
    pass

admin.site.register(User, UserAdmin)