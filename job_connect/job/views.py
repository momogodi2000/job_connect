from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetView
from .models import CustomUser, AbstractUser
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import RegistrationForm
import yagmail
from .models import Contact
from .forms import ContactForm, PortfolioForm
from campay.sdk import Client as CamPayClient
from django.http import FileResponse
from django.utils.timezone import now
from .models import Receipt  # Make sure to import your Receipt model
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.graphics.barcode.qr import QrCodeWidget
from io import BytesIO
from campay.sdk import Client as CamPayClient
from .models import Communication  # Ensure this import is present
from django.http import HttpResponse  # Import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Communication
from .models import CustomUser, Review
from django.http import JsonResponse
from .forms import ReviewForm
from django.contrib.auth.forms import PasswordResetForm
import os
from django.utils.crypto import get_random_string  # Add this line



# Replace with your Gmail credentials
username = "yvangodimomo@gmail.com"
password = "pzls apph esje cgdl"

# Create a yagmail object
yag = yagmail.SMTP(username, password)



# Authentication view


def home(request):
    return render(request, 'home/home.html')


def services(request):
    return render(request, 'home/services.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('contact')  # Redirect to the same page after saving
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})


def about(request):
    return render(request, 'home/about.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
          
            if user.role == 'admin':
                return redirect('admin_panel')  # Adjust this to match your URL pattern name
            elif user.role == 'expert':
                return redirect('expert_panel')   
            else:
                return redirect('clients_panel')  # Adjust this to match your URL pattern name
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})



User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code = get_random_string(length=6)  # Generate a random code
            
            # Send email with reset code
            yag = yagmail.SMTP("yvangodimomo@gmail.com", "pzls apph esje cgdl")
            yag.send(to=email, subject="Password Reset Code", contents=f"Your reset code is: {reset_code}")

            # Store the reset code in the session temporarily
            request.session['reset_code'] = reset_code
            request.session['user_email'] = email
            
            return redirect('verify_reset_code')  # Redirect to code verification page
        except User.DoesNotExist:
            messages.error(request, "Email not associated with any account.")
    
    return render(request, 'auth/forgot_password.html')

def verify_reset_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        if entered_code == request.session.get('reset_code'):
            return redirect('reset_password')  # Redirect to reset password page
        else:
            messages.error(request, "Invalid reset code.")
    
    return render(request, 'auth/verify_reset_code.html')

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        email = request.session.get('user_email')
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password reset successfully.")
        return redirect('login')  # Redirect to login after successful reset
    
    return render(request, 'auth/reset_password.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot_password.html'  # Specify your template here
    success_url = reverse_lazy('password_reset_done')  # Redirect after a successful reset request
    email_template_name = 'password_reset_email.html'  # Template for the password reset email



@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')


##  dashboard

@login_required
def expert_panel(request):
    return render(request, 'panel/expert/expert_panel.html')

@login_required
def admin_panel(request):
    return render(request, 'panel/admin/admin_panel.html')



@login_required
def clients_panel(request):
    return render(request, 'panel/clients/clients_panel.html')


## expert_panel

@login_required
def profile_overview(request):
    return render(request, 'panel/expert/profile/profile_overview.html', {'user': request.user})


@login_required
def security_settings(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        profile_picture = request.FILES.get('profile_picture')

        # Update name and email
        request.user.name = name
        request.user.email = email

        # Check current password for security
        if not request.user.check_password(current_password):
            context = {'error': 'Current password is incorrect'}
        else:
            # Update password if provided and valid
            if new_password and new_password == confirm_password:
                request.user.set_password(new_password)

            # Update profile picture if provided
            if profile_picture:
                request.user.profile_picture = profile_picture

            request.user.save()
            context = {'success': 'Settings updated successfully'}
            # Redirect to avoid resubmission on refresh
            return redirect('user_panel')
    else:
        context = {}

    return render(request, 'panel/expert/profile/security_settings.html', context)

def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Portfolio will be created with 'payment_status' as 'not_paid'
            return redirect('payment_page')  # Redirect to the payment page
    else:
        form = PortfolioForm()
    
    return render(request, 'panel/expert/portfoloi/create_portfolio.html', {'form': form})


User = get_user_model()

# Set up CamPay client with credentials
campay = CamPayClient({
    "app_username": "JByBUneb4BceuEyoMu1nKlmyTgVomd-QfokOrs4t4B9tPJS7hhqUtpuxOx5EQ7zpT0xmYw3P6DU6LU0mH2DvaQ",
    "app_password": "m-Xuj9EQIT_zeQ5hSn8hLjYlyJT7KnSTHABYVp7tKeHKgsVnF0x6PEcdtZCVaDM0BN5mX-eylX0fhrGGMZBrWg",
    "environment": "PROD"  # use "DEV" for demo mode or "PROD" for live mode
})



def payment_page(request):
    if request.method == 'POST':
        user = request.user
        phone = request.POST.get("phone", "").strip()
        name = user.get_full_name()
        email = user.email

        # Ensure phone is formatted correctly
        if not phone.startswith('237'):
            phone = '237' + phone

        # Make the real API call to CamPay for payment collection
        collect_response = campay.collect({
            "amount": "5",
            "currency": "XAF",
            "from": phone,
            "description": "Portfolio fees",
            "external_reference": "",  # Unique reference can be set here
        })

        # Handle success or failure
        if collect_response.get('status') == 'SUCCESSFUL':
            # Find the latest portfolio created by the user (assuming only one per session)
            portfolio = Portfolio.objects.filter(email=email).last()
            if portfolio:
                portfolio.payment_status = 'paid'  # Update payment status
                portfolio.save()  # Save the updated portfolio

            # Store receipt information
            receipt_info = {
                "amount": "10",
                "currency": "XAF",
                "user": user,
                "date": now(),
                'reference': collect_response.get('reference'),
                'external_reference': collect_response.get('external_reference'),
                "from_number": phone,
                "description": "PORTFOLIO FEES",
                "name": name,
                "email": email,
            }

            # Create a Receipt object (assuming you have a Receipt model)
            receipt = Receipt.objects.create(**receipt_info)

            # Generate PDF receipt
            buffer = generate_pdf_file(receipt_info)
            response = FileResponse(buffer, as_attachment=True, filename=f'receipt_{receipt.id}.pdf', content_type='application/pdf')
            return response

        else:
            # Handle payment failure
            reason = collect_response.get('reason', collect_response.get('message', 'An error occurred with the payment, please try later.'))
            context = {'message': reason}
            return render(request, 'panel/expert/payment/payment_page.html', context)

    return render(request, 'panel/expert/payment/payment_page.html')

def generate_pdf_file(payment_receipt_info):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Create a PDF document
    p.drawString(100, 750, "Payment Receipt For Portfolio Fees")

    y = 700
    receipt_fields = [
        f"Reference: {payment_receipt_info['reference']}",
        f"User: {payment_receipt_info['name']}",
        f"Phone Number: {payment_receipt_info['from_number']}",
        f"Fees: {payment_receipt_info['amount']} {payment_receipt_info['currency']}",
        f"Description: {payment_receipt_info['description']}",
        f"Date: {payment_receipt_info['date']}",
    ]

    for field in receipt_fields:
        p.drawString(100, y, field)
        y -= 20

    # QR code generation (if needed)
    qrcode_info = "\n".join(receipt_fields)
    qrw = QrCodeWidget(qrcode_info)
    b = qrw.getBounds()
    w = b[2] - b[0]
    h = b[3] - b[1]
    d = Drawing(400, 400, transform=[45. / w, 0, 0, 56. / h, 0, 0])
    d.add(qrw)
    renderPDF.draw(d, p, 1, 1)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
from django.shortcuts import render
from .models import Portfolio, Region, Town, Quarter
from django.db.models import Q

def portfolio_list_view(request):
    selected_region = request.GET.get('region')
    selected_town = request.GET.get('town')
    selected_quarter = request.GET.get('quarter')

    portfolios = Portfolio.objects.all()
    
    if selected_region:
        selected_region = int(selected_region)  # Convert to integer
        portfolios = portfolios.filter(region_id=selected_region)
    
    if selected_town:
        selected_town = int(selected_town)  # Convert to integer
        portfolios = portfolios.filter(town_id=selected_town)
    
    if selected_quarter:
        selected_quarter = int(selected_quarter)  # Convert to integer
        portfolios = portfolios.filter(quarter_id=selected_quarter)

    regions = Region.objects.all()
    towns = Town.objects.all()
    quarters = Quarter.objects.all()

    context = {
        'portfolios': portfolios,
        'regions': regions,
        'towns': towns,
        'quarters': quarters,
        'selected_region': selected_region,
        'selected_town': selected_town,
        'selected_quarter': selected_quarter,
    }

    return render(request, 'panel/expert/view_portfoloi/portfolio_list.html', context)


from django.contrib import messages

def pay_now(request, service_type):
    # Simulate a payment process
    prices = {
        'standard': 2000,
        'premium': 20000,
        'vip': 35000
    }
    
    # Get the service price based on the type
    price = prices.get(service_type, None)
    
    if price:
        # In a real-world scenario, you would integrate with a payment gateway here
        # For now, simulate a successful payment
        receipt = {
            'service_type': service_type,
            'price': price,
            'user': request.user,  # Assuming user is logged in
            'transaction_id': 'TXN' + str(request.user.id) + service_type.upper(),
        }
        
        # Optionally show a success message
        messages.success(request, f'Payment for {service_type.capitalize()} service was successful!')
        
        # Redirect to a receipt page after payment
        return render(request, 'panel/expert/payment/receipt.html', {'receipt': receipt})
    
    # If service_type is invalid, show an error
    return HttpResponse("Invalid service type", status=400)



def community_page(request):
    return render(request, 'panel/expert/communication/community.html')


from .models import ForumMessage
import json
from django.utils import timezone
from datetime import timedelta  # Add this line if it's not already present



def forum_view(request):
    if request.method == 'GET':
        # Get messages from the last 7 days
        time_threshold = timezone.now() - timedelta(days=7)
        messages = ForumMessage.objects.filter(timestamp__gte=time_threshold).order_by('-timestamp')
        online_users = User.objects.filter(is_active=True)
        return render(request, 'panel/expert/communication/forum/forum.html', {'messages': messages, 'online_users': online_users})

def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_text = data.get('message')
        file = request.FILES.get('file')  # Handle file input
        
        # Ensure file size is under 3MB
        if file and file.size > 3 * 1024 * 1024:
            return JsonResponse({'status': 'error', 'message': 'File size exceeds the 3MB limit'})
        
        forum_message = ForumMessage.objects.create(
            user=request.user,
            message=message_text,
            file=file
        )
        return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})

def get_messages(request):
    # Fetch messages from the last 7 days
    time_threshold = timezone.now() - timedelta(days=7)
    messages = ForumMessage.objects.filter(timestamp__gte=time_threshold).order_by('-timestamp')

    message_list = [{
        'user': message.user.username,
        'message': message.message,
        'file': message.file.url if message.file else None,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    } for message in messages]

    return JsonResponse({'messages': message_list})

def get_online_users(request):
    # Fetch active users
    online_users = User.objects.filter(is_active=True)
    users_list = [{'username': user.username} for user in online_users]

    return JsonResponse({'users': users_list})



from .models import Networking
from .forms import NetworkingForm

# View for networking form
def networking_form_view(request):
    if request.method == 'POST':
        form = NetworkingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('job_seeker_list')  # Redirect to the job seeker list
    else:
        form = NetworkingForm()
    return render(request, 'panel/expert/communication/forum/networking_form.html', {'form': form})

# View for listing job seekers
def job_seeker_list_view(request):
    job_seekers = Networking.objects.all()
    return render(request, 'panel/expert/communication/forum/job_seeker_list.html', {'job_seekers': job_seekers})


@login_required
def profile_admin(request):
    return render(request, 'panel/admin/profile/profile_admin.html', {'user': request.user})



from .models import JobPost, JobApplication

def job_applications(request):
    job_posts = JobPost.objects.filter(is_active=True)
    applications = JobApplication.objects.filter(candidate_email=request.user.email)
    
    saved_jobs = []  # Logic to get saved jobs if implemented
    # Fetch saved jobs if you have a model for that or define logic accordingly

    return render(request, 'panel/expert/find/job_applications.html', {
        'job_posts': job_posts,
        'applications': applications,
        'saved_jobs': saved_jobs,
    })

from django.views.decorators.csrf import csrf_exempt
from .models import JobApplication


@csrf_exempt
def apply_job(request):
    if request.method == 'POST':
        job_post_id = request.POST.get('job_post_id')
        candidate_name = request.POST.get('candidate_name')  # Get from form
        candidate_email = request.POST.get('candidate_email')  # Get from form
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter')
        applied_at = timezone.now()  # Automatically set to current date

        application = JobApplication.objects.create(
            job_post_id=job_post_id,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            resume=resume,
            cover_letter=cover_letter,
            applied_at=applied_at  # Set the application date
        )

        return JsonResponse({'message': 'Application submitted successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.db.models import Count, Avg


def analytics_view(request):
    # Example Analytics
    job_application_performance = JobApplication.objects.values('job_post__title').annotate(total_applications=Count('id'))
    
    client_feedback = Review.objects.all()
    average_rating = Review.objects.aggregate(average_rating=Avg('rating'))['average_rating']

    context = {
        'job_application_performance': job_application_performance,
        'client_feedback': client_feedback,
        'average_rating': average_rating,
    }

    return render(request, 'panel/expert/analyse/analytics.html', context)



##admin panel


@login_required
def user_management(request):
    users = CustomUser.objects.all()
    return render(request, 'panel/admin/manage_user/user_management.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = RegistrationForm()
    return render(request, 'panel/admin/manage_user/user_management.html', {'form': form})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = RegistrationForm(instance=user)
    return render(request, 'panel/admin/manage_user/edit_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_management')
    return render(request, 'panel/admin/manage_user/confirm_delete.html', {'user': user})


def post_communication(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        photo = request.FILES.get('photo')
        date = timezone.now()  # Automatically set the current date

        # Create a new Communication instance
        communication = Communication(title=title, description=description, photo=photo, date=date)
        communication.save()

        messages.success(request, 'Communication posted successfully!')
        return redirect('post_communication')  # Redirect to the same page or another page

    current_date = timezone.now().date()  # Get the current date for the form
    return render(request, 'panel/admin/communication/post_communication.html', {'current_date': current_date})

from .models import Portfolio, Receipt

def portfolio_management(request):
    portfolios = Portfolio.objects.all()
    receipts = {receipt.user.id: receipt for receipt in Receipt.objects.all()}  # Create a dictionary for faster lookup
    return render(request, 'panel/admin/communication/portfolio_management.html', {'portfolios': portfolios, 'receipts': receipts})

def delete_candidate(request, candidate_id):
    # Ensure the request method is POST to avoid accidental deletions
    if request.method == 'POST':
        candidate = get_object_or_404(Portfolio, id=candidate_id)
        candidate.delete()
        return redirect('some_view_name')  # Redirect to a list view or success page
    
    # If not a POST request, return a bad request response
    return HttpResponseBadRequest("Invalid request")




# Yagmail credentials
username = "yvangodimomo@gmail.com"
password = "pzlsapphesjecgdl"  # Use your app-specific password

# Create a yagmail object
yag = yagmail.SMTP(username, password)

def manage_contact(request):
    contacts = Contact.objects.all()  # Fetch all contact messages
    return render(request, 'panel/admin/contact/manage_contact.html', {'contacts': contacts})

def reply_contact(request, contact_id):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send the reply email
        yag.send(
            to=email,
            subject='Reply to Your Contact Message',
            contents=message
        )

        return redirect('manage_contact')

def delete_contact(request, contact_id):

    contact = Contact.objects.get(id=contact_id)
    contact.delete()
    return redirect('manage_contact')


@login_required
def security(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        profile_picture = request.FILES.get('profile_picture')

        # Update name and email
        request.user.name = name
        request.user.email = email

        # Check current password for security
        if not request.user.check_password(current_password):
            context = {'error': 'Current password is incorrect'}
        else:
            # Update password if provided and valid
            if new_password and new_password == confirm_password:
                request.user.set_password(new_password)

            # Update profile picture if provided
            if profile_picture:
                request.user.profile_picture = profile_picture

            request.user.save()
            context = {'success': 'Settings updated successfully'}
            # Redirect to avoid resubmission on refresh
            return redirect('user_panel')
    else:
        context = {}

    return render(request, 'panel/admin/profile/security.html', context)




## clients panel



# Communication list view
def communication_list(request):
    communications = Communication.objects.all()
    return render(request, 'panel/clients/communications/communication_list.html', {'communications': communications})

# Communication detail view
def communication_detail(request, pk):
    communication = get_object_or_404(Communication, pk=pk)
    return render(request, 'panel/clients/communications/communication_detail.html', {'communication': communication})

# Download communication as PDF
def download_communication_pdf(request, pk):
    communication = get_object_or_404(Communication, pk=pk)
    html_string = render_to_string('panel/clients/communications/communication_pdf.html', {'communication': communication})
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{communication.title}.pdf"'
    return response



@login_required
def expert_list(request):
    experts = CustomUser.objects.filter(role='expert')
    return render(request, 'panel/clients/reviews/expert_list.html', {'experts': experts})

@login_required
def rate_expert(request, expert_id):
    expert = get_object_or_404(CustomUser, pk=expert_id, role='expert')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.expert = expert
            review.client_name = request.user.get_full_name()
            review.client_email = request.user.email
            review.save()
            return redirect('expert_list')
    else:
        form = ReviewForm()

    return render(request, 'panel/clients/reviews/rate_expert.html', {'expert': expert, 'form': form})


def view_comments(request, expert_id):
    expert = get_object_or_404(CustomUser, id=expert_id, role='expert')
    reviews = Review.objects.filter(expert=expert)
    return render(request, 'panel/clients/reviews/view_comments.html', {'expert': expert, 'reviews': reviews})


from .models import JobPost, JobApplication
from .forms import JobPostForm, JobApplicationForm

# View for creating a new job posting
@login_required
def create_job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.posted_by = request.user
            job_post.save()
            return redirect('manage_jobs')
    else:
        form = JobPostForm()
    return render(request, 'panel/clients/post/create_job_post.html', {'form': form})

# View for managing job postings
@login_required
def manage_jobs(request):
    job_posts = JobPost.objects.filter(posted_by=request.user)
    return render(request, 'panel/clients/post/manage_jobs.html', {'job_posts': job_posts})

# View to handle applications
@login_required
def track_applications(request, job_post_id):
    job_post = get_object_or_404(JobPost, id=job_post_id, posted_by=request.user)
    applications = JobApplication.objects.filter(job_post=job_post)
    return render(request, 'panel/clients/post/track_applications.html', {'job_post': job_post, 'applications': applications})

def edit_job_post(request, job_id):
    job_post = get_object_or_404(JobPost, id=job_id)
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            return redirect('manage_jobs')  # Redirect after successful edit
    else:
        form = JobPostForm(instance=job_post)
    
    return render(request, 'panel/clients/post/edit_job_post.html', {'form': form, 'job_post': job_post})

from .models import JobPost

def toggle_job_status(request, job_id):
    job_post = get_object_or_404(JobPost, id=job_id)
    # Toggle the status (assuming you have a boolean field 'is_active' in the JobPost model)
    job_post.is_active = not job_post.is_active
    job_post.save()
    return redirect('manage_jobs')  # Redirect back to job management page




@login_required
def load_messages(request):
    user_id = request.GET.get('user_id')
    recipient = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(sender=request.user, recipient=recipient) | \
               Message.objects.filter(sender=recipient, recipient=request.user)
    return render(request, 'panel/clients/discuss/messages.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        recipient = get_object_or_404(CustomUser, id=recipient_id)
        message_text = request.POST.get('message')
        file = request.FILES.get('file', None)

        # Save the message
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            body=message_text,
            file=file,
            created_at=timezone.now()
        )

        return JsonResponse({
            'message': f"Message from {message.sender.username} to {message.recipient.username}",
            'message_body': message.body
        })
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def messaging(request):
    # Assuming you're passing a list of users for messaging
    users = CustomUser.objects.exclude(id=request.user.id)  # Exclude the current user
    return render(request, 'panel/clients/discuss/messages.html', {'users': users})


@login_required
def profile_view(request):
    return render(request, 'panel/clients/profile/profile_view.html', {'user': request.user})


@login_required
def setting(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        profile_picture = request.FILES.get('profile_picture')

        # Update name and email
        request.user.name = name
        request.user.email = email

        # Check current password for security
        if not request.user.check_password(current_password):
            context = {'error': 'Current password is incorrect'}
        else:
            # Update password if provided and valid
            if new_password and new_password == confirm_password:
                request.user.set_password(new_password)

            # Update profile picture if provided
            if profile_picture:
                request.user.profile_picture = profile_picture

            request.user.save()
            context = {'success': 'Settings updated successfully'}
            # Redirect to avoid resubmission on refresh
            return redirect('user_panel')
    else:
        context = {}

    return render(request, 'panel/clients/profile/setting.html', context)



from django.shortcuts import render
from django.http import JsonResponse
from .models import EducationalLevel, Domain, Specification, Region, Town, Quarter, Portfolio

def candidate_search(request):
    education_levels = EducationalLevel.objects.all()
    domains = Domain.objects.all()
    regions = Region.objects.all()
    return render(request, 'panel/clients/job/candidate_search.html', {
        'education_levels': education_levels,
        'domains': domains,
        'regions': regions
    })

def get_specifications(request):
    domain_id = request.GET.get('domain_id')
    specifications = Specification.objects.filter(domain_id=domain_id)
    return JsonResponse(list(specifications.values('id', 'name')), safe=False)

def get_towns(request):
    region_id = request.GET.get('region_id')
    towns = Town.objects.filter(region_id=region_id)
    return JsonResponse(list(towns.values('id', 'name')), safe=False)

def get_quarters(request):
    town_id = request.GET.get('town_id')
    quarters = Quarter.objects.filter(town_id=town_id)
    return JsonResponse(list(quarters.values('id', 'name')), safe=False)

def search_candidates(request):
    education_level = request.GET.get('education_level')
    domain = request.GET.get('domain')
    specification = request.GET.get('specification')
    region = request.GET.get('region')
    town = request.GET.get('town')
    quarter = request.GET.get('quarter')

    candidates = Portfolio.objects.all()
    if education_level:
        candidates = candidates.filter(educational_level_id=education_level)
    if domain:
        candidates = candidates.filter(domain_id=domain)
    if specification:
        candidates = candidates.filter(specification_id=specification)
    if region:
        candidates = candidates.filter(region_id=region)
    if town:
        candidates = candidates.filter(town_id=town)
    if quarter:
        candidates = candidates.filter(quarter_id=quarter)

    return render(request, 'panel/clients/job/candidate_results.html', {'candidates': candidates})


from .models import CustomUser, Review, Booking
from django.utils import timezone

def candidate_details(request, expert_id):
    expert = get_object_or_404(CustomUser, id=expert_id, role='expert')
    reviews = Review.objects.filter(expert=expert)
    
    if request.method == 'POST':
        # Handle booking request
        booking_date = request.POST.get('date')
        service_description = request.POST.get('service_description')

        booking = Booking.objects.create(
            client=request.user,
            expert=expert,
            date=booking_date,
            service_description=service_description
        )
        return redirect('candidate_search') 

       ## return JsonResponse({'message': 'Booking request submitted successfully!'})

    return render(request, 'panel/clients/job/candidate_detail.html', {'expert': expert, 'reviews': reviews})

