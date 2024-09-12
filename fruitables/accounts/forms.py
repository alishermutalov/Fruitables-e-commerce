from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="Email", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter Email', 
            'class': 'form-control'
        })
    )
    
    username = forms.CharField(
        required=True, 
        label="Username", 
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Username', 
            'class': 'form-control'
        })
    )
    
    password1 = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Password', 
            'class': 'form-control'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password', 
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username", widget=forms.TextInput(attrs={"placeholder":"Enter email or username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter your password"}), label="Password")



class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address']

    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile