from django.contrib import admin
from models import TimeLine 

class TimeLineAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'content', 'date_published',)

admin.site.register(TimeLine, TimeLineAdmin)
