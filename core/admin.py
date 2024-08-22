from django.contrib import admin
from .models import BDUser

@admin.register(BDUser)
class BDUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_tel', 'user_email', 'user_role')
    search_fields = ('user__first_name', 'user__last_name', 'user_tel', 'user_email')
