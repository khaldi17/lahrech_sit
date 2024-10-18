from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
import datetime as t
from .models import Contact, Blog  # Ensure your models are imported
from django.contrib.auth.decorators import user_passes_test
from .forms import BlogForm  # Assuming you've created a form for Blog
from django.contrib.auth.models import User

# Commands for Django management
# python3 manage.py create_groups  
# python3 manage.py runserver 0.0.0.0:8000
# python3 manage.py makemigrations
# python3 manage.py migrate 

# Home view
def home_view(request):
    return render(request, 'index.html',{'superadmin': request.user.is_superuser, })

# Blog list view
def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blog.html', {'blogs': blogs})

# Blog detail view
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog.html', {'blog': blog})  # Separate template for details

# Reservation form handling
def resarve(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        day = request.POST.get('day')  # Should be in string format like "Sunday", "Monday"
        time = request.POST.get('time')
        message = request.POST.get('message')

        # Calculate the actual date based on the current day of the week
        today = t.date.today()  # Get today's date
        day_mapping = {
            'Sunday': 6,
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5
        }  # Mapping days to weekday indexes

        if day in day_mapping:
            target_day = today + t.timedelta((day_mapping[day] - today.weekday()) % 7)
        else:
            messages.error(request, 'Invalid day selected.')
            return render(request, 'index.html', {'error': 'Invalid day selected'})

        # Count the number of reservations for the selected day and time
        number = Contact.objects.filter(day=target_day, time=time).count() + 1

        # Create the new reservation
        Contact.objects.create(name=name, phone=phone, day=target_day, time=time, message=message, number=number)

        # Prepare data for the success page
        context = {
            'number': number,
            'name': name,
            'phone': phone,
            'day': day,
            'time': time,
            'message': message
        }

        # Redirect with success message and render the success page
        messages.success(request, 'Reservation successful!')
        return render(request, 'reservation_success.html', context)  # Render success page with context

    # If not POST, render the index page or any other relevant page
    return render(request, 'index.html')
    

# View to display the reservations table
def reservation_table(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        today = t.date.today()  # Get today's date
        day_mapping = {
            'Sunday': 6,
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5
        }  # Mapping days to weekday indexes

        if day in day_mapping:
            target_day = today + t.timedelta((day_mapping[day] - today.weekday()) % 7)
        else:
            messages.error(request, 'Invalid day selected.')
            return render(request, 'reserve.html')

        table = Contact.objects.filter(day=target_day)
        return render(request, 'reserve.html', {'table': table})
    else:
        return render(request, 'reserve.html')

# Class-based view for sending emails
@method_decorator(csrf_exempt, name='dispatch')
class MailerView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construct email content
        email_subject = f"New Message from {name}: {subject}"
        email_body = (
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{message}"
        )

        try:
            # Send the email
            send_mail(
                email_subject,
                email_body,
                'your_email@example.com',  # From email
                ['recipient@example.com'],  # Replace with the recipient's email
                fail_silently=False,
            )
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

# Check if user is superadmin
def is_superadmin(user):
    return user.is_superuser

@user_passes_test(is_superadmin)
def blog_create(request):
    authors = User.objects.all()  # Get all users as possible authors

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog')  # Redirect to blog list after creation
    else:
        form = BlogForm()

    context = {
        'form': form,
        'superadmin': request.user.is_superuser,
        'authors': authors,  # Pass the authors to the template
    }
    return render(request, 'blog_create.html', context)