from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
import datetime

def index(request):
    return render(request, "mainapp/index.html")

def stu_login(request):
    return render(request, "mainapp/stulogin.html")

def lib_login(request):
    return render(request, "mainapp/liblogin.html")

def lib(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        libSet = librarian.objects.all()
        is_there = False
        for f in libSet:
            if f.username == username and f.password == password:
                is_there = True
            if is_there:
                return HttpResponseRedirect(reverse('lib_home', kwargs={'lib':username}))

def lib_home(request, lib):
    libSet = librarian.objects.all()
    l = libSet.get(username = lib)
    return render(request, "mainapp/libhome.html",{
        "l": l
    })

def add(request, lib):
    if request.method == "POST":
        name = request.POST["name"]
        phoneno = request.POST["phoneNo"]
        email = request.POST["email"]
        enrollNo = request.POST["enrollNo"]
        username = request.POST["username"]
        password = request.POST["password"]
        p2 = request.POST["password2"]
        l = librarian.objects.get(username = lib)
        if password == p2:
            s = student(name=name, mobileNumber=phoneno, emailId=email, enrollmentNumber=enrollNo, username=username, password=password)
            s.save()
            return HttpResponseRedirect(reverse('add', kwargs={'lib': l.username}))
    else:
        l = librarian.objects.get(username = lib)
        return render(request, "mainapp/add.html", {
            "l": l
        })


def stu(request):

    if request.method == "POST":
        un = request.POST["username"]
        ps = request.POST["password"]
        stuSet = student.objects.all()
        is_there = False
        for f in stuSet:
            if f.username == un and f.password == ps:
                is_there = True
        if is_there:
            return HttpResponseRedirect(reverse('stu_home', kwargs={'stu': un}))

def stu_home(request, stu):
    s = student.objects.get(username = stu)
    return render(request, "mainapp/stuhome.html", {
        "s":s
    })

def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        phoneno = request.POST["phoneNo"]
        email = request.POST["email"]
        enrollNo = request.POST["enrollNo"]
        username = request.POST["username"]
        password = request.POST["password"]
        p2 = request.POST["password2"]
        if password == p2:
            s = NewStudent(name=name, mobileNumber=phoneno, emailId=email, enrollmentNumber=enrollNo, username=username, password=password)
            s.save()
            return HttpResponseRedirect(reverse('register'))
    else:
        return render(request, "mainapp/register.html")

def requestList(request, lib):
    l = librarian.objects.get(username= lib)
    newStuSet = NewStudent.objects.all()
    return render(request, "mainapp/NewStuList.html", {
        "list": newStuSet,
        "l": l
    })

def add2(request, lib, stuId):
    if request.method == "POST":
        name = request.POST["name"]
        phoneno = request.POST["phoneNo"]
        email = request.POST["email"]
        enrollNo = request.POST["enrollNo"]
        username = request.POST["username"]
        password = request.POST["password"]
        s = student(name=name, mobileNumber=phoneno, emailId=email, enrollmentNumber=enrollNo, username=username, password=password)
        s.save()
        d = NewStudent.objects.get(id= stuId)
        d.delete()
        return HttpResponseRedirect(reverse('requestList', kwargs={'lib': lib}))
    else:
        l = librarian.objects.get(username=lib)
        s = NewStudent.objects.get(id = stuId)
        return render(request, "mainapp/add2.html",{
            "l": l, 
            "s": s
        })

def stu_search(request, stu):
    booklist = Book.objects.all()
    return render(request, "mainapp/stu_search.html", {
        "booklist": booklist,
        "stu": stu
    })

def book(request, stu):
    if request.method == 'POST':
        b = Book.objects.get(bookName=request.POST["book"])
        authors = b.Authors.all()
        c = b.Copies_of_book.count()
        bcopies = b.Copies_of_book.all()
        a=0
        r = 0
        booklist = Book.objects.all()
        for bc in bcopies:
            if bc.BookAvalibilityStatus:
                a = a+1
            if bc.BookReserverdStatus:
                r = r+1
        return render(request, "mainapp/book.html",{
            "b":b,
            "stu": stu,
            "c": c,
            "authors": authors,
            "a": a, 
            "r": r,
            "booklist": booklist
        })

def book2(request, stu, b):
    s = student.objects.get(username = stu)
    bk = Book.objects.get(id = b)
    bcopies = bk.Copies_of_book.all()
    bId = 0
    for book in bcopies:
        if book.BookAvalibilityStatus:
            bId = book.id
            break
    bookcopy = BookDataBase.objects.get(id=bId)
    bookcopy.Student = s
    bookcopy.BookAvalibilityStatus = False
    bookcopy.BookIssuedate = datetime.datetime.now()
    bookcopy.BookDuedate = bookcopy.BookIssuedate + datetime.timedelta(days=30)
    bookcopy.save()
    return HttpResponseRedirect(reverse('stu_search', kwargs={'stu': s.username}))

def stu_books(request, stu):
    Takenbooklist = student.objects.get(name=stu).Taken_Books.all()
    Reserverdlist = student.objects.get(name=stu).Reserverd_Books.all()
    return render(request, "mainapp/stu_books.html",{
        "tbl": Takenbooklist,
        "rbl": Reserverdlist,
        "stu":stu
    })

def stu_fine(request, stu):
    Takenbooklist = student.objects.get(username=stu).Taken_Books.all()
    now = datetime.datetime.now()
    return render(request, "mainapp/stu_fine.html", {
        "tbl": Takenbooklist,
        "stu":stu,
        "now": now
    })

def extension(request, stu):
    Takenbooklist = student.objects.get(username=stu).Taken_Books.all()
    return render(request, "mainapp/extension.html", {
        "stu":stu,
        "tbl": Takenbooklist
    })

def extend(request, stu, bId):
    book = BookDataBase.objects.get(id=bId)
    Takenbooklist = student.objects.get(username=stu).Taken_Books.all()
    if book.BookReserverdStatus:
        return   
    else:
        book.BookDuedate = book.BookDuedate + datetime.timedelta(days=10)
        book.save()
        msg = "Sucessfully Extended"
        return render(request, "mainapp/extension.html", {
        "stu":stu,
        "tbl": Takenbooklist,
        "msg": msg
    })


        





    
