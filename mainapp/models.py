from django.db import models
from django import forms


class librarian(models.Model):
    name = models.CharField(max_length=64)
    mobileNumber = models.IntegerField(blank=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    emailId = models.CharField(max_length=64)
    loginStatus = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} Ph.no:{self.mobileNumber}"

class student(models.Model):
    name = models.CharField(max_length=64)
    mobileNumber = models.IntegerField(blank = True)
    emailId = models.CharField(max_length=64, blank = True)
    enrollmentNumber = models.IntegerField(blank=False)
    loginStatus = models.BooleanField(default=False)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} Ph.no:{self.mobileNumber}"

class NewStudent(models.Model):
    name = models.CharField(max_length=64)
    mobileNumber = models.IntegerField(blank = True)
    emailId = models.CharField(max_length=64, blank = True)
    enrollmentNumber = models.IntegerField(blank=False)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    password2 = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} Enrollment No:{self.enrollmentNumber}"


