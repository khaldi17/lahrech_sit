from django.urls import path
from . import views
from .views import MailerView

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('mailer/', MailerView.as_view(), name='mailer_view'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),  # Blog detail view
    path('resarve',views.resarve , name='resarve'),
    path('reservation_table',views.reservation_table, name='reservation_table'),
    path('blog/create/', views.blog_create, name='blog_create'),
]
