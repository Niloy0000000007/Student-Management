from django.contrib import admin
from .models import Student, Course, Subject, Attendance

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Attendance)


