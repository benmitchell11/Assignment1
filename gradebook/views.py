import pandas
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView

from Assignment1 import settings
from .mixins import AdminRequiredMixin, LecturerRequiredMixin, StudentRequiredMixin
from .models import Semester, Class, Course, Student, User, Lecturer, StudentEnrolment
from .forms import SemesterForm, StudentForm, LecturerForm, CourseForm, ClassForm, StudentEnrolmentForm, \
    LecturerAssignmentForm, AssignGradeForm


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


class ClassDetailView(DetailView):
    model = Class
    template_name = 'class_detail.html'


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
        user = student.user.first_name
        response = super().delete(request, *args, **kwargs)
        user.delete()
        return response


class LecturerListView(AdminRequiredMixin, ListView):
    model = Lecturer
    template_name = 'lecturer_list.html'
    ordering = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


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
        user = request.user
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)


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


class StudentDashboardView(StudentRequiredMixin, View):
    template_name = 'student_dashboard.html'

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        context = {
            'student': student,
        }
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


class LecturerDashboardView(LecturerRequiredMixin, TemplateView):
    template_name = 'lecturer_dashboard.html'

    def get(self, request, *args, **kwargs):
        lecturer = Lecturer.objects.get(user=request.user)
        context = {
            'lecturer': lecturer,
        }
        return render(request, self.template_name, context)


class StudentEnrolmentView(View):
    def get(self, request, pk):
        class_instance = get_object_or_404(Class, pk=pk)
        form = StudentEnrolmentForm(initial={'classID': class_instance})
        return render(request, 'student_enrol.html', {'form': form, 'class_instance': class_instance})

    def post(self, request, pk):
        class_instance = get_object_or_404(Class, pk=pk)
        form = StudentEnrolmentForm(request.POST)
        if form.is_valid():
            student_enrolment = form.save(commit=False)
            student_enrolment.classID = class_instance
            student_enrolment.save()
            return redirect('class_detail', pk=pk)
        return render(request, 'student_enrol.html', {'form': form, 'class_instance': class_instance})


class AssignLecturerView(AdminRequiredMixin, View):
    def get(self, request, pk):
        class_instance = get_object_or_404(Class, pk=pk)
        form = LecturerAssignmentForm(instance=class_instance, course_id=class_instance.course_id)
        return render(request, 'assign_lecturer.html', {'form': form, 'class_instance': class_instance})

    def post(self, request, pk):
        class_instance = get_object_or_404(Class, pk=pk)
        form = LecturerAssignmentForm(request.POST, instance=class_instance, course_id=class_instance.course_id)
        if form.is_valid():
            form.save()
            return redirect('class_detail', pk=pk)
        return render(request, 'assign_lecturer.html', {'form': form, 'class_instance': class_instance})


class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['enrolments'] = StudentEnrolment.objects.filter(student=student)
        return context


class LecturerDetailView(DetailView):
    model = Lecturer
    template_name = 'lecturer_detail.html'
    context_object_name = 'lecturer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lecturer = self.get_object()
        context['classes'] = Class.objects.filter(lecturer=lecturer)
        return context


class SemesterDetailView(DetailView):
    model = Semester
    template_name = 'semester_detail.html'
    context_object_name = 'semester'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        semester = self.get_object()
        context['classes'] = Class.objects.filter(semester=semester)
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['classes'] = Class.objects.filter(course=course)
        context['lecturers'] = Lecturer.objects.filter(course=course)
        return context


class AssignGradeView(LecturerRequiredMixin, UpdateView):
    model = StudentEnrolment
    form_class = AssignGradeForm
    template_name = 'assign_grade.html'

    def form_valid(self, form):
        form.instance.grade_time = timezone.now()
        self.object = form.save()
        self.send_email_notification()
        return super().form_valid(form)

    def send_email_notification(self):
        class_number = str(self.object.classID.number)
        subject = 'Grade Updated Notification'
        message = ('Your grade for ' + self.object.classID.course.code + ' ' + class_number +
                   ' has been posted.')
        from_email = settings.EMAIL_HOST_USER
        to_email = self.object.student.user.email

        send_mail(subject, message, from_email, [to_email])

    def get_success_url(self):
        return reverse('class_detail', kwargs={'pk': self.object.classID.pk})


def read_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        worksheet = pandas.read_excel(excel_file)
        data = pandas.DataFrame(worksheet, columns=['email', 'first_name', 'last_name', 'dob'])

        for index, row in data.iterrows():
            email = row['email']
            first_name = row['first_name']
            last_name = row['last_name']
            dob = row['dob']

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password="12345"
            )

            student = Student.objects.create(
                user=user,
                dob=dob,

            )

        print('Students created successfully')
        return render(request, 'upload_students.html', {'msg': 'Students created successfully'})
    else:
        return render(request, 'upload_students.html', {'msg': ''})


class CheckGradesView(StudentRequiredMixin, ListView):
    model = StudentEnrolment
    template_name = 'check_grades.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return StudentEnrolment.objects.filter(student=self.request.user.student)


class EnrolledClassesView(StudentRequiredMixin, ListView):
    model = Class
    template_name = 'view_enrolled_classes.html'
    context_object_name = 'enrolled_classes'

    def get_queryset(self):
        return StudentEnrolment.objects.filter(student=self.request.user.student)


class AssignedClassesView(LecturerRequiredMixin, ListView):
    model = Class
    template_name = 'assigned_classes.html'
    context_object_name = 'assigned_classes'

    def get_queryset(self):
        lecturer = self.request.user.lecturer.id
        return Class.objects.filter(lecturer=lecturer)
