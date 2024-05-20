from django.contrib import admin

# Register your models here.
from .models import StudentEnrolment


@admin.register(StudentEnrolment)
class StudentEnrolmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'classID', 'grade')  # Define fields to display in the list view
    search_fields = ('student__username', 'classID__course_code')  # Define fields for search functionality
