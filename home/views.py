from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import Contact_lib,Book,Register,Book_request
from datetime import datetime
from django.contrib import messages
import json
import os
from decimal import Decimal
from django.http import HttpResponse
from django.db.models import Q




# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_form(request):
    return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(username=username)
            if user.password == password:
                request.session['username'] = user.username
                request.session['role'] = user.role
                messages.success(request, f"Welcome, {user.username}")
                return redirect('index') 
            else:
                messages.success(request, "Incorrect password")
        except Register.DoesNotExist:
            messages.success(request, "User not found")

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact_lib(name=name,email=email,phone=phone,message=message,date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
    # return HttpResponse("This is the contact page")
    return render(request,'contact.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')  # 'admin' or 'user'

        if password1 != password2:
            messages.success(request, "Passwords do not match.")
            return redirect('register')

        if Register.objects.filter(username=username).exists():
            messages.success(request, "Username already taken.")
            return redirect('register')

        register_user = Register.objects.create(
            username=username,
            email=email,
            password=password1, 
            role=role
        )
        register_user.save()
        messages.success(request, "Registration successful.")
        return redirect('login')

    return render(request, 'register.html')

def contact_list(request):
    contacts = Contact_lib.objects.all()
    return render(request, 'msg_list.html', {'contacts': contacts})

def book_list(request):
    if 'username' not in request.session:
        messages.warning(request, "Please login to view books.")
        return redirect('login')
    
    lists = Book.objects.all()
    return render(request, 'book_list.html', {'books': lists})

def request_book(request, book_id):
    username = request.session.get('username')
    book = get_object_or_404(Book, id=book_id)
    user = get_object_or_404(Register, username=username)
    
    existing_request = Book_request.objects.filter(user=user, book=book, status='P').first()
    request_count = Book_request.objects.filter(Q(user=user) & Q(status__in=['Pending', 'Approved'])).count()
    if existing_request:
        messages.warning(request, "You have already requested this book!")
        return redirect('book_list')
    if request_count >= 2:
        messages.info(request, "You have already requested for two books")
        return redirect('book_list')
    
    Book_request.objects.create(user=user, book=book)

    book.is_available = False
    book.save()
    
    messages.success(request, "Request sent to admin for approval!")
    return redirect('book_list')
    
def book_request_list(request):
    requests = Book_request.objects.all().select_related('book', 'user')
    return render(request, 'book_request.html', {'requests': requests})

def approve_request(request, request_id):
    req = get_object_or_404(Book_request, id=request_id)
    req.status = 'Approved'
    req.save()
    messages.success(request, f"Book request for '{req.book.title}' approved!")
    return redirect('book_request_list')

def reject_request(request, request_id):
    req = get_object_or_404(Book_request, id=request_id)
    req.status = 'Rejected'
    req.save()
    messages.error(request, f"Book request for '{req.book.title}' rejected!")
    return redirect('book_request_list')


def book_detail(request, book_id):
    username = request.session.get('username')
    book = get_object_or_404(Book, id=book_id)

    already_requested_or_assigned = False
    if username:
        user = get_object_or_404(Register, username=username)
        already_requested_or_assigned = Book_request.objects.filter(
            book=book,
            user=user,
            status__in=["Pending", "Approved", "assigned"]
        ).exists()

    return render(request, "book_details.html", {
        "book": book,
        "already_requested_or_assigned": already_requested_or_assigned
    })

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        image = request.FILES.get('image')
        created_at = request.POST.get('created_at')
        isbn_no = request.POST.get('isbn_no')
        publish = request.POST.get('publish')
        is_available = request.POST.get('is_available') == 'on'  # checkbox
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')

        # Save book to the database
        book = Book(
            title=title,
            author=author,
            image=image,
            created_at=created_at,
            isbn_no=isbn_no,
            publish=publish,
            is_available=is_available,
            description=description,
            price=price,
            category=category
        )
        book.save()

        messages.success(request, "Book added successfully.")
        return redirect('book_list')  # Replace with your actual book list view name

    return render(request, 'add_book.html')
  
def book_add(request):
    return render(request,'add_book.html')     

def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.isbn_no = request.POST.get('isbn_no')
        book.publish = request.POST.get('publish')
        book.created_at = request.POST.get('created_at')
        book.price = request.POST.get('price')
        book.category = request.POST.get('category')
        book.is_available = request.POST.get('is_available') == 'True'
        book.description = request.POST.get('description')

        # Check if new image uploaded
        if request.FILES.get('image'):
            book.image = request.FILES.get('image')

        book.save()
        messages.success(request, "Book updated successfully.")
        return redirect('book_list')  # or your book list page

    return render(request, 'update_book.html', {'book': book})

def book_update(request):
    return render(request, 'update_book.html')

def about(request):
    return render(request,'about.html')
    
    
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, "Book deleted successfully.")
    return redirect('book_list')  # change to your actual book list view name

# def import_books_from_json(request):
    with open('UserProject/books.json', 'r', encoding='utf-8') as file:
        books = json.load(file)

    for item in books:
        try:
            # Convert price safely
            price = Decimal(str(item['price']).replace('₹', '').strip())

            Book.objects.create(
                title=item['title'],
                author=item['author'],
                image=item['image'],
                created_at=item['created_at'],
                isbn_no=item['isbn_no'],
                publish=item['publish'],
                is_available=str(item.get('is_available', False)).lower() in ['true', '1'],
                description=item['description'],
                price=price,
                category=item['category']
            )
        except Exception as e:
            return HttpResponse(f"❌ Error: {str(e)}")

    return HttpResponse("✅ All books imported successfully")