from django.contrib import admin

from ta_scheduler.models import Course, Section, User, CourseInstructor, PublicProfile, PrivateProfile

# Register your models here.

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(User)
admin.site.register(CourseInstructor)
admin.site.register(PublicProfile)
admin.site.register(PrivateProfile)