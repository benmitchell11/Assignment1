from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .mixins import AdminRequiredMixin
from .models import Semester, Class, Course, Student, User, Lecturer, StudentEnrolment
from .forms import SemesterForm, StudentForm, LecturerForm, CourseForm, ClassForm, StudentEnrolmentForm


class SemesterListView(AdminRequiredMixin, ListView):
    model = Semester
    template_name = 'semester_list.html'
    ordering = 'id'


class CreateSemesterView(AdminRequiredMixin, CreateView):
    model = Semester
    template_name = 'create_semester.html'
    form_class = SemesterForm
    success_url = reverse_lazy('semester_list')


class UpdateSemesterView(AdminRequiredMixin, UpdateView):
    model = Semester
    template_name = 'update_semester.html'
    form_class = SemesterForm
    success_url = reverse_lazy('semester_list')


class DeleteSemesterView(AdminRequiredMixin, DeleteView):
    model = Semester
    template_name = 'delete_semester.html'
    success_url = reverse_lazy('semester_list')


class ClassListView(AdminRequiredMixin, ListView):
    model = Class
    template_name = 'class_list.html'
    ordering = 'id'


class CreateClassView(AdminRequiredMixin, CreateView):
    model = Class
    template_name = 'create_class.html'
    form_class = ClassForm
    success_url = reverse_lazy('class_list')


class UpdateClassView(AdminRequiredMixin, UpdateView):
    model = Class
    template_name = 'update_class.html'
    fields = ['number', 'semester', 'course', 'lecturer']
    success_url = reverse_lazy('class_list')


class DeleteClassView(AdminRequiredMixin, DeleteView):
    model = Class
    template_name = 'delete_class.html'
    success_url = reverse_lazy('class_list')


class CourseListView(AdminRequiredMixin, ListView):
    model = Course
    template_name = 'course_list.html'
    ordering = 'id'


class CreateCourseView(AdminRequiredMixin, CreateView):
    model = Course
    template_name = 'create_course.html'
    form_class = CourseForm
    success_url = reverse_lazy('course_list')


class UpdateCourseView(AdminRequiredMixin, UpdateView):
    model = Course
    template_name = 'update_course.html'
    form_class = CourseForm
    success_url = reverse_lazy('course_list')


class DeleteCourseView(AdminRequiredMixin, DeleteView):
    model = Course
    template_name = 'delete_course.html'
    success_url = reverse_lazy('course_list')


class StudentListView(AdminRequiredMixin, ListView):
    model = Student
    template_name = 'student_list.html'
    ordering = 'id'


class CreateStudentView(AdminRequiredMixin, CreateView):
    model = Student
    template_name = 'create_student.html'
    form_class = StudentForm
    success_url = reverse_lazy('student_list')


class UpdateStudentView(AdminRequiredMixin, UpdateView):
    model = Student
    template_name = 'update_student.html'
    form_class = StudentForm
    success_url = reverse_lazy('student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        context['form'] = StudentForm(instance=student)
        return context


class DeleteStudentView(AdminRequiredMixin, DeleteView):
    model = Student
    template_name = 'delete_student.html'
    success_url = reverse_lazy('student_list')

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        user = student.user
        user.delete()  # Delete the corresponding user
        return super().delete(request, *args, **kwargs)


class LecturerListView(AdminRequiredMixin, ListView):
    model = Lecturer
    template_name = 'lecturer_list.html'
    ordering = 'id'


class CreateLecturerView(AdminRequiredMixin, CreateView):
    model = Lecturer
    template_name = 'create_lecturer.html'
    form_class = LecturerForm
    success_url = reverse_lazy('lecturer_list')


class UpdateLecturerView(AdminRequiredMixin, UpdateView):
    model = Lecturer
    template_name = 'update_lecturer.html'
    form_class = LecturerForm
    success_url = reverse_lazy('lecturer_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lecturer = self.object
        context['form'] = LecturerForm(instance=lecturer)
        context['user_data'] = lecturer.user
        return context


class DeleteLecturerView(AdminRequiredMixin, DeleteView):
    model = Lecturer
    template_name = 'delete_lecturer.html'
    success_url = reverse_lazy('lecturer_list')

    def delete(self, request, *args, **kwargs):
        lecturer = self.get_object()
        user = lecturer.user
        user.delete()
        return super().delete(request, *args, **kwargs)


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class AdminLoginView(View):
    template_name = 'admin_login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Invalid credentials or not an admin')
        return render(request, self.template_name, {'form': form})


class AdminDashboardView(AdminRequiredMixin, View):
    template_name = 'admin_dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def signout(request):
    logout(request)
    return redirect(reverse('home'))


class LecturerLoginView(View):
    template_name = 'lecturer_login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            if Lecturer.objects.filter(user=user).exists():
                login(request, user)
                return redirect('lecturer_dashboard')
            else:
                context = {'error_message': 'You do not have permission to access this page.'}
                return render(request, self.template_name, context)
        else:
            context = {'error_message': 'Invalid credentials. Please try again.'}
            return render(request, self.template_name, context)


class StudentLoginView(View):
    template_name = 'student_login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            if Student.objects.filter(user=user).exists():
                login(request, user)
                return redirect('student_dashboard')
            else:
                context = {'error_message': 'You do not have permission to access this page.'}
                return render(request, self.template_name, context)
        else:
            context = {'error_message': 'Invalid credentials. Please try again.'}
            return render(request, self.template_name, context)


class StudentEnrollView(AdminRequiredMixin, CreateView):
    model = StudentEnrolment
    template_name = 'student_enrol.html'
    form_class = StudentEnrolmentForm
    success_url = reverse_lazy('admin_dashboard')
