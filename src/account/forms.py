from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import UserBase


class RegistrationForm(forms.ModelForm):
    """Create a registration form with few mandatory fields."""

    # mandatory username
    user_name = forms.CharField(
        label="Enter Username", min_length=4, max_length=50, help_text="Required"
    )

    # mandatory email and password
    email = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email."},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = (
            "user_name",
            "email",
        )

    # get unique and clean username, password and email
    def clean_username(self):
        user_name = self.cleaned_data["user_name"].lower()

        # access user table and match if the username that user entered
        # matches with the usernames in users table form UserBase
        # if the count is 1 then raise error else return the username
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists!")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match!")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists! Please use another email or Login."
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update(
            {"class": "input w-full", "placeholder": "Username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "input w-full", "placeholder": "E-mail"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "input w-full", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "input w-full", "placeholder": "Confirm Password"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Username",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )


class UserEditForm(forms.ModelForm):
    user_name = forms.CharField(
        label="Username",
        min_length=4,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Username",
                "id": "form-username",
                "readonly": "readonly",
            }
        ),
    )

    email = forms.EmailField(
        label="Account email (cannot be changed)",
        widget=forms.EmailInput(
            attrs={
                "class": "input w-full",
                "id": "form-email",
                "readonly": "readonly",
                "placeholder": "Email",
            }
        ),
    )

    first_name = forms.CharField(
        label="First name",
        max_length=150,
        min_length=4,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "First Name",
                "id": "form-firstname",
            }
        ),
    )

    class Meta:
        model = UserBase
        fields = (
            "user_name",
            "email",
            "first_name",
        )

    # some fields needs to filled necessarily by the user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=250,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Email",
                "id": "form-email",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "Unfortunately we cannot find the email address"
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input w-full",
                "placeholder": "New Password",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Confirm Password",
            }
        ),
    )
