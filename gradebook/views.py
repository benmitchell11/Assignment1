from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Semester, Class, Course, Student, User, Lecturer
from .forms import SemesterForm, StudentForm, LecturerForm


class SemesterListView(ListView):
    model = Semester
    template_name = 'semester_list.html'
    ordering = 'id'


class CreateSemesterView(CreateView):
    model = Semester
    template_name = 'create_semester.html'
    fields = ['name', 'year']
    success_url = reverse_lazy('semester_list')


class UpdateSemesterView(UpdateView):
    model = Semester
    template_name = 'update_semester.html'
    fields = ['name', 'year']
    success_url = reverse_lazy('semester_list')


class DeleteSemesterView(DeleteView):
    model = Semester
    template_name = 'delete_semester.html'
    success_url = reverse_lazy('semester_list')


class ClassListView(ListView):
    model = Class
    template_name = 'class_list.html'
    ordering = 'id'


class CreateClassView(CreateView):
    model = Class
    template_name = 'create_class.html'
    fields = ['number', 'semester', 'course', 'lecturer']
    success_url = reverse_lazy('class_list')


class UpdateClassView(UpdateView):
    model = Class
    template_name = 'update_class.html'
    fields = ['number', 'semester', 'course', 'lecturer']
    success_url = reverse_lazy('class_list')


class DeleteClassView(DeleteView):
    model = Class
    template_name = 'delete_class.html'
    success_url = reverse_lazy('class_list')


class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    ordering = 'id'


class CreateCourseView(CreateView):
    model = Course
    template_name = 'create_course.html'
    fields = ['number', 'semester', 'course', 'lecturer']
    success_url = reverse_lazy('course_list')


class UpdateCourseView(UpdateView):
    model = Course
    template_name = 'update_course.html'
    fields = ['number', 'semester', 'course', 'lecturer']
    success_url = reverse_lazy('course_list')


class DeleteCourseView(DeleteView):
    model = Course
    template_name = 'delete_course.html'
    success_url = reverse_lazy('course_list')


class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    ordering = 'id'


class CreateStudentView(CreateView):
    model = Student
    template_name = 'create_student.html'
    form_class = StudentForm
    success_url = reverse_lazy('student_list')


class UpdateStudentView(UpdateView):
    model = Student
    template_name = 'update_student.html'
    fields = ['first_name', 'last_name', 'email', 'dob', 'password']
    success_url = reverse_lazy('student_list')


class DeleteStudentView(DeleteView):
    model = Student
    template_name = 'delete_student.html'
    success_url = reverse_lazy('student_list')

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        user = student.user
        user.delete()  # Delete the corresponding user
        return super().delete(request, *args, **kwargs)


class LecturerListView(ListView):
    model = User
    template_name = 'lecturer_list.html'
    ordering = 'id'


class CreateLecturerView(CreateView):
    model = Lecturer
    template_name = 'create_lecturer.html'
    form_class = LecturerForm
    success_url = reverse_lazy('lecturer_list')


class UpdateLecturerView(UpdateView):
    model = Lecturer
    template_name = 'update_lecturer.html'
    fields = ['first_name', 'last_name', 'email', 'dob', 'password', 'course']
    success_url = reverse_lazy('lecturer_list')


class DeleteLecturerView(DeleteView):
    model = Lecturer
    template_name = 'delete_lecturer.html'
    success_url = reverse_lazy('lecturer_list')

    def delete(self, request, *args, **kwargs):
        lecturer = self.get_object()
        user = lecturer.user
        user.delete()
        return super().delete(request, *args, **kwargs)


