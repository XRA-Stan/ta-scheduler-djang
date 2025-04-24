from django.contrib import admin

from ta_scheduler.models import Course, Section, User

# Register your models here.

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(User)
