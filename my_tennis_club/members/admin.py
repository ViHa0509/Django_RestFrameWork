from django.contrib import admin
from .models import CustomUser
# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", 'joined_date', 'phone')

admin.site.register(CustomUser, MemberAdmin)
