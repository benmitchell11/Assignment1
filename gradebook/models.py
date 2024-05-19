from django.db import models
from django.contrib.auth.models import User


class Semester(models.Model):
    number = models.IntegerField()
    year = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)


class Class(models.Model):
    number = models.IntegerField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()


class StudentEnrolment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    enrol_time = models.DateTimeField(auto_now_add=True)
    grade_time = models.DateTimeField(auto_now=True)
    classID = models.ForeignKey(Class, on_delete=models.CASCADE)



