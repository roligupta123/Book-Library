from django.db import models

# Create your models here.
class Contact_lib(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    message = models.CharField()
    date = models.DateField()

    def __str__(self):
        return self.name
        
        


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    isbn_no = models.CharField(max_length=13)
    publish = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    description = models.TextField()
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class Register(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=50, default='User')  # Default role is 'User'
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Book_request(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # Status can be 'Pending', 'Approved', 'Rejected'

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"