from django import forms
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
