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



def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetView.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_done')  # Redirect to success page
    else:
        form = CustomPasswordResetView.form_class()

    return render(request, 'auth/forgot_password.html', {'form': form})

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