from django.contrib import admin
from home.models import Contact_lib,Book,Register,Book_request
# Register your models here.

admin.site.register(Contact_lib)
admin.site.register(Book)
admin.site.register(Register)
admin.site.register(Book_request)