from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('login',views.user_login,name="login"),
    path('logout',views.user_logout,name="logout"),
    path('contact',views.contact,name="contact"),
    path('login_form',views.login_form,name="login_form"),
    path('register',views.register,name="register"),
    path('msg_list',views.contact_list,name="list"),
    path('book_list', views.book_list, name='book_list'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add_book', views.add_book, name='add_book'),
    path('book_add', views.book_add, name='book_add'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('update_book/<int:book_id>/', views.update_book, name='update_book'),
    path('book_update', views.book_update, name='book_update'),
    path('about/', views.about, name='about'),
    path('assign/<int:book_id>/', views.request_book, name='assign'),
    path('book_requests/', views.book_request_list, name='book_request_list'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
]
