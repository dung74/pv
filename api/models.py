
# Create your models here.
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Parent(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

class Student(models.Model):
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    current_grade = models.IntegerField()
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='students')

class Class(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'),
        ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday'),
    ]
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    time_slot = models.TimeField() # Giả định giờ bắt đầu
    teacher_name = models.CharField(max_length=255)
    max_students = models.IntegerField()

class Subscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    total_sessions = models.IntegerField()
    used_sessions = models.IntegerField(default=0)

    @property
    def is_valid(self):
        return self.end_date >= timezone.now().date() and self.used_sessions < self.total_sessions

class ClassRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True) 
    # Cần thêm field ngày học cụ thể để check logic 24h khi xóa
    scheduled_for = models.DateTimeField()