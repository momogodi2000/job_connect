from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser
from django.contrib.auth.models import User
from .models import Contact
from .models import Portfolio




class RegistrationForm(UserCreationForm):
    ROLES = [
        ('client', 'Client'),
        ('expert', 'Expert'),
    ]
    role = forms.ChoiceField(choices=ROLES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'description', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            'name', 'email', 'address', 'phone', 'age', 'created_at', 'profile_photo',
            'years_of_experience', 'educational_level', 'specification',
            'domain', 'region', 'town', 'quarter'
        ]

    # Overriding the save method to automatically set 'created_at' to the current datetime
    def save(self, commit=True):
        portfolio = super().save(commit=False)
        if not portfolio.created_at:  # Check if created_at is not already set
            portfolio.created_at = now()  # Automatically set created_at to the current time
        if commit:
            portfolio.save()
        return portfolio
        
    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:  # Limit to 5MB
                raise forms.ValidationError("Profile photo size must be under 5MB.")
        return photo


from .models import Region, Town, Quarter

class PortfolioFilterForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Region")
    town = forms.ModelChoiceField(queryset=Town.objects.all(), required=False, label="Town")
    quarter = forms.ModelChoiceField(queryset=Quarter.objects.all(), required=False, label="Quarter")


from .models import Networking

class NetworkingForm(forms.ModelForm):
    class Meta:
        model = Networking
        fields = ['domain', 'specification', 'location', 'description', 'age', 'resume', 'email', 'facebook']
        widgets = {
            'domain': forms.Select(attrs={'class': 'form-select'}),
            'specification': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
        }
