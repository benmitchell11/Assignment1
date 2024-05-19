from django import forms
from django.contrib.auth.models import User

from .models import Semester, Class, Course, Student, Lecturer


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['number', 'year']


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['number', 'semester', 'course', 'lecturer']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'dob']

    def save(self, commit=True):
        user = User.objects.create_user(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            username=self.cleaned_data['username']
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student




class LecturerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Lecturer
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'course', 'dob']

    def save(self, commit=True):
        user = User.objects.create_user(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            username=self.cleaned_data['username']
        )
        lecturer = super().save(commit=False)
        lecturer.user = user
        if commit:
            lecturer.save()
        return lecturer



