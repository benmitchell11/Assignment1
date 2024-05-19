from django.urls import path
from . import views

urlpatterns = [
    path('semesters/', views.SemesterListView.as_view(), name='semester_list'),
    path('semesters/create/', views.CreateSemesterView.as_view(), name='create_semester'),
    path('semesters/delete/<int:pk>/', views.DeleteSemesterView.as_view(), name='delete_semester'),
    path('/semesters/update/<int:pk>/', views.UpdateSemesterView.as_view(), name='update_semester'),
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('classes/create/', views.CreateClassView.as_view(), name='create_class'),
    path('classes/delete/<int:pk>/', views.DeleteClassView.as_view(), name='delete_class'),
    path('/classes/update/<int:pk>/', views.UpdateClassView.as_view(), name='update_class'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CreateCourseView.as_view(), name='create_course'),
    path('courses/delete/<int:pk>/', views.DeleteCourseView.as_view(), name='delete_course'),
    path('/courses/update/<int:pk>/', views.UpdateCourseView.as_view(), name='update_course'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/create/', views.CreateStudentView.as_view(), name='create_student'),
    path('students/delete/<int:pk>/', views.DeleteStudentView.as_view(), name='delete_student'),
    path('/students/update/<int:pk>/', views.UpdateStudentView.as_view(), name='update_student'),
    path('lecturers/', views.LecturerListView.as_view(), name='lecturer_list'),
    path('lecturers/create/', views.CreateLecturerView.as_view(), name='create_lecturer'),
    path('lecturers/delete/<int:pk>/', views.DeleteLecturerView.as_view(), name='delete_lecturer'),
    path('/lecturers/update/<int:pk>/', views.UpdateLecturerView.as_view(), name='update_lecturer'),
    # Add other URLs for updating, deleting, and showing semesters as needed
]