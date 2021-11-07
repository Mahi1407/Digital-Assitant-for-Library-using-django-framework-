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
            else:
                msg = 'Invalid Credentials'
                return render(request, "mainapp/liblogin.html",{
                    'msg': msg
                })

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
            msg= s.name+" got successfully added to the portal"
            s.save()
            return render(request, "mainapp/add.html", {
                "l":l, 
                "msg": msg
            })
        else:
            msg = "Password doesn't match with Re-enter Password"
            return render(request, "mainapp/add.html", {
                "l":l, 
                "msg": msg
            })
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
        else:
            msg = 'Invalid Credentials'
            return render(request, "mainapp/stulogin.html",{
                'msg': msg
            })

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
        msg = f"{s.name}({s.enrollmentNumber}) got successfully added to the portal"
        s.save()
        d = NewStudent.objects.get(id= stuId)
        d.delete()
        l = librarian.objects.get(username= lib)
        newStuSet = NewStudent.objects.all()
        return render(request, 'mainapp/NewStuList.html', {
            "list": newStuSet,
            "l": l,
            "msg": msg
        })
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
    tbl = s.Taken_Books.all()
    is_there = False
    for t in tbl:
        if bk == t.Book:
            is_there = True
    if is_there:
        authors = bk.Authors.all()
        c = bk.Copies_of_book.count()
        bcopies = bk.Copies_of_book.all()
        a=0
        r = 0
        booklist = Book.objects.all()
        msg = "Selected Book is already present in your Taken Book list"
        for bc in bcopies:
            if bc.BookAvalibilityStatus:
                a = a+1
            if bc.BookReserverdStatus:
                r = r+1
        return render(request, "mainapp/book.html",{
            "b":bk,
            "stu": stu,
            "c": c,
            "authors": authors,
            "a": a, 
            "r": r,
            "booklist": booklist,
            "msg": msg
        })
        

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
    s = student.objects.get(username=stu)
    Takenbooklist = student.objects.get(username=stu).Taken_Books.all()
    ntb = s.Taken_Books.count()
    Reserverdlist = student.objects.get(username=stu).Reserverd_Books.all()
    nrb = s.Reserverd_Books.count()
    return render(request, "mainapp/stu_books.html",{
        "tbl": Takenbooklist,
        "rbl": Reserverdlist,
        "stu":stu,
        "ntb": ntb,
        "nrb": nrb
    })

def Overduedays(a, b, c):
    dt = datetime.date(a, b, c)
    now = datetime.datetime.now()
    nowdt = now.date()
    if dt>=nowdt:
        return 0
    else:
        return (nowdt-dt).days

def fine(a, b, c):
    return Overduedays(a, b, c)*2

def stu_fine(request, stu):
    Takenbooklist = student.objects.get(username=stu).Taken_Books.all()
    total_fine= 0
    for b in Takenbooklist:
        f = fine(b.BookDuedate.year, b.BookDuedate.month,  b.BookDuedate.day)
        total_fine+=f
    now = datetime.datetime.now()
    return render(request, "mainapp/stu_fine.html", {
        "tbl": Takenbooklist,
        "stu":stu,
        "now": now, 
        'total_fine': total_fine
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
    now = datetime.datetime.now()   
    nowdt = now.date()
    if nowdt>book.BookDuedate.date():
        msg = "The Duedate for the book has been crossed: Can't Extend the Due date"
        return render(request, "mainapp/extension.html", {
            "stu":stu,
            "tbl": Takenbooklist,
            "msg": msg
        } )
    if book.BookReserverdStatus:
        msg = "Requested Book is reserved by another student: Can't Extend the Due date"
        return render(request, "mainapp/extension.html", {
            "stu":stu,
            "tbl": Takenbooklist,
            "msg": msg
        } )
    else:
        book.BookDuedate = book.BookDuedate + datetime.timedelta(days=10)
        if (book.BookDuedate.date()-book.BookIssuedate.date()).days>40:
            msg ="Can't Extend the Due date more than once"
            return render(request, "mainapp/extension.html", {
                "stu":stu,
                "tbl": Takenbooklist,
                "msg": msg
            } )
        else:
            msg = book.Book.bookName+" got Sucessfully Extended"
            book.save()
            return render(request, "mainapp/extension.html", {
                "stu":stu,
                "tbl": Takenbooklist,
                "msg": msg
            })

def add_bookcopy(request, lib):
    booklist = Book.objects.all()
    if request.method == "POST":
        isbn = request.POST["isbn"]
        b = Book.objects.get(bookName=request.POST["book"])
        book = BookDataBase(BookIsbnNumber=isbn , Book=b)
        book.save()
        msg = b.bookName+" with ISBN code "+isbn+" got successfully added to the DataBase"
        return render(request, "mainapp/add_bookcopy.html", {
            "booklist": booklist,
            "lib":lib,
            "msg": msg
        })
    return render(request, "mainapp/add_bookcopy.html", {
        "booklist": booklist,
        "lib":lib
    })

def add_author(request, lib):
    if request.method=="POST":
        name = request.POST["author"]
        Edu = request.POST["edudetails"]
        a = Author(name=name, Education=Edu)
        a.save()
        msg = name+" got successfully added to Authors List"
        return render(request, "mainapp/add_author.html", {
            "lib":lib,
            "msg": msg
        })

    return render(request, "mainapp/add_author.html", {
        "lib":lib
    })

def add_newbook(request, lib):
    al = Author.objects.all()
    return render(request, "mainapp/add_newbook.html", {
        "lib": lib,
        "al": al
    })

def create_book(request, lib):
    if request.method == "POST":
        bookname = request.POST["bookname"]
        publication = request.POST["publication"]
        edition = request.POST["edition"] 
        b = Book(bookName=bookname, publication=publication, edition=edition)
        b.save()
        return render(request, "mainapp/addauthors_to_book.html", {
            "lib":lib,
            "b": b,
            "authors": b.Authors.all(),
            "non_authors": Author.objects.exclude(Written_Books=b).all()
        })

def addauthor_to_book(request, lib, bId):
    if request.method == "POST":
        a = Author.objects.get(name=request.POST["author"]) 
        b = Book.objects.get(id=bId)
        b.Authors.add(a)
        return render(request, "mainapp/addauthors_to_book.html", {
            "lib":lib,
            "b":b,
            "authors": b.Authors.all(),
            "non_authors": Author.objects.exclude(Written_Books=b).all()
        })

def lib_return(request, lib):
    return render(request, "mainapp/returnBook.html", {
        'lib':lib
    })

def return_book(request, lib):
    if request.method == "POST":
        isbn = int(request.POST["isbn"])
        bkl = BookDataBase.objects.all()
        is_there = False
        for b in bkl:
            if b.BookIsbnNumber==isbn:
                is_there = True
        if is_there==False:
            msg = f"Book with ISBN code '{isbn}' doesn't exist"
            return render(request, "mainapp/returnBook.html", {
                "lib":lib, 
                "msg": msg
            })
        b = BookDataBase.objects.get(BookIsbnNumber= request.POST["isbn"])
        return render(request, "mainapp/returnBook.html", {
        'lib':lib,
        "b":b
    })

def book_returned(request, lib, bId):
    b = BookDataBase.objects.get(id = bId)
    msg = ""
    if b.BookReserverdStatus == False:
        b.BookAvalibilityStatus = True
        b.Student = None
        b.BookDuedate = None
        b.BookIssuedate = None
        b.save()
        msg = f"Book with ISBN number '{b.BookIsbnNumber}' got successfully returned"

    return render(request, "mainapp/returnBook.html", {
        'lib':lib,
        'msg':msg,
        'b':b
    })

def lib_delete(request, lib):
    sl = student.objects.all()
    return render(request, "mainapp/delete_stu.html", {
        "sl":sl,
        "lib":lib
    })

def get_stu(request, lib):
    if request.method == "POST":
        stu = request.POST["student"]
        sl = student.objects.all()
        is_there = False
        for st in sl:
            if st.name==stu:
                is_there = True
        if is_there:
            s = student.objects.get(name=request.POST["student"])
            tbl = s.Taken_Books.all()
            return render(request, "mainapp/delete_stu.html", {
                'lib':lib,
                's': s,
                "tbl": tbl,
                "sl": sl,
            })
        msg = f"Student with name '{stu}' doesn't exist"
        return render(request, "mainapp/delete_stu.html", {
        "sl":sl,
        "lib":lib,
        "msg":msg
    })
        

def delete_stu(request, lib, stuId):
    stu = student.objects.get(id=stuId)
    msg = stu.name+" got successfully removed from the database"
    stbl = stu.Taken_Books.all()
    srbl = stu.Reserverd_Books.all()
    for b in stbl:
        b.BookDuedate = None
        b.BookIssuedate = None
        b.BookAvalibilityStatus = True
        b.save()
    
    for r in srbl:
        r.BookReserverdStatus = False
    stu.delete()
    sl = student.objects.all()
    return render(request,  "mainapp/delete_stu.html", {
        "sl": sl,
        "lib": lib, 
        "msg":msg
    })

def delete_req(request, lib, stuId):
    l = librarian.objects.get(username= lib)
    newStuSet = NewStudent.objects.all()
    d = NewStudent.objects.get(id= stuId)
    msg = "Request from "+d.name+" got successfully deleted"
    d.delete()
    return render(request, 'mainapp/NewStuList.html', {
        "list": newStuSet,
        "l": l,
        "msg": msg
    })

def display_books(request, lib):
    booklist = BookDataBase.objects.all()
    return render(request, "mainapp/display_books.html", {
        "lib":lib, 
        "bl": booklist
    })

def delete_bookcpy(request, lib, bId):
    bkl = BookDataBase.objects.all()
    is_there = False
    for b in bkl:
        if b.id == bId:
            is_there = True
    if is_there == False:
        return render(request, "mainapp/display_books.html", {
        "lib":lib, 
        "bl": bkl,
    })
    b = BookDataBase.objects.get(id = bId)
    msg = f"Book {b.Book.bookName} with Isbn code '{b.BookIsbnNumber}' got successfully removed from the database"
    b.delete()
    booklist = BookDataBase.objects.all()
    return render(request, "mainapp/display_books.html", {
        "lib":lib, 
        "bl": booklist,
        "msg": msg
    })


        
 




    
