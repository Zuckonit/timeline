from django.contrib import admin
from models import UserProfile

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'birthday', 'sex', 'age', 'priority')

admin.site.register(UserProfile, AccountAdmin)
