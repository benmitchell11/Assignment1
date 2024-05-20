from django import forms
from django.contrib.auth.models import User

from .models import Semester, Class, Course, Student, Lecturer, StudentEnrolment


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['semester', 'year']
        labels = {
            'semester': 'Semester Number',
        }


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'number', 'semester', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
        self.fields['course'].label_from_instance = lambda obj: "%s (%s)" % (obj.name, obj.code)
        self.fields['semester'].queryset = Semester.objects.all()
        self.fields['semester'].label_from_instance = lambda obj: "%s (%s)" % (obj.semester, obj.year)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class AssignGradeForm(forms.ModelForm):
    class Meta:
        model = StudentEnrolment
        fields = ['grade']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = ['email', 'password', 'first_name', 'last_name', 'dob']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('password')
            user_data = self.instance.user
            self.fields['first_name'].initial = user_data.first_name
            self.fields['last_name'].initial = user_data.last_name
            self.fields['email'].initial = user_data.email

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.pk:
            user = instance.user
            if 'password' in self.cleaned_data:
                user.set_password(self.cleaned_data['password'])
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        else:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            instance.user = user

        if commit:
            instance.save()
        return instance




class LecturerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Lecturer
        fields = ['email', 'password', 'first_name', 'last_name', 'course', 'dob']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('password')
            user_data = self.instance.user
            self.fields['first_name'].initial = user_data.first_name
            self.fields['last_name'].initial = user_data.last_name
            self.fields['email'].initial = user_data.email

        self.fields['course'].queryset = Course.objects.all()
        self.fields['course'].label_from_instance = lambda obj: obj.code

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.pk:
            user = instance.user
            if 'password' in self.cleaned_data:
                user.set_password(self.cleaned_data['password'])
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
        else:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            instance.user = user

        if commit:
            instance.save()
        return instance






class StudentEnrolmentForm(forms.ModelForm):
    class Meta:
        model = StudentEnrolment
        fields = ['student']

    def __init__(self, *args, **kwargs):
        super(StudentEnrolmentForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class': 'form-control'})
        self.fields['student'].label_from_instance = lambda obj: f"{obj.user.first_name} {obj.user.last_name}"




class LecturerAssignmentForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['lecturer']

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id', None)
        super().__init__(*args, **kwargs)
        if course_id:
            self.fields['lecturer'].queryset = Lecturer.objects.filter(course__id=course_id)
        else:
            self.fields['lecturer'].queryset = Lecturer.objects.all()
        self.fields['lecturer'].label_from_instance = lambda obj: f"{obj.user.first_name} {obj.user.last_name}"
