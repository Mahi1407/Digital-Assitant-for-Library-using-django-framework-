from django.db import models
from django import forms


class librarian(models.Model):
    name = models.CharField(max_length=64, unique=True)
    mobileNumber = models.IntegerField(blank=True, unique=True)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=15)
    emailId = models.CharField(max_length=64, unique=True)
    loginStatus = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} Ph.no:{self.mobileNumber}"

    def getusername(self):
        return self.username

class student(models.Model):
    name = models.CharField(max_length=64, unique=True)
    mobileNumber = models.IntegerField(blank = True, unique=True)
    emailId = models.CharField(max_length=64, blank = True, unique = True)
    enrollmentNumber = models.IntegerField(blank=False, unique=True)
    loginStatus = models.BooleanField(default=False)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.mobileNumber})"

class NewStudent(models.Model):
    name = models.CharField(max_length=64)
    mobileNumber = models.IntegerField(blank = True)
    emailId = models.CharField(max_length=64, blank = True)
    enrollmentNumber = models.IntegerField()
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    password2 = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.enrollmentNumber})"

class Author(models.Model):
    name = models.CharField(max_length=64)
    Education = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    Authors = models.ManyToManyField(Author, blank=True, related_name="Written_Books")
    bookName = models.CharField(max_length=100)
    publication = models.CharField(max_length=100)
    edition = models.IntegerField(blank=True)
    
    def __str__(self):
        return f"{self.bookName}, {self.Authors.all()}"
        

class BookDataBase(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="Copies_of_book")
    BookIsbnNumber = models.IntegerField(unique=True)
    BookAvalibilityStatus = models.BooleanField(default=True)
    BookReserverdStatus = models.BooleanField(default=False)
    BookIssuedate = models.DateTimeField(null=True)
    BookDuedate = models.DateTimeField(null=True)
    Student = models.ForeignKey(student, on_delete=models.SET_NULL, related_name="Taken_Books", null=True, blank=True)
    Reserved_Stu = models.ForeignKey(student, on_delete=models.SET_NULL, related_name="Reserverd_Books", null=True, blank=True)

    def __str__(self):
        return f"({self.BookIsbnNumber}){self.Book.bookName}, {self.Book.Authors.all()}"


