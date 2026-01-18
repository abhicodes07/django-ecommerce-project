from django import forms
from django_countries import Countries

STATES = [("CA", "California"), ("CH", "Chicago")]


class BillingAddressForm(forms.Form):
    name = forms.CharField(
        label="Customer Name",
        min_length=4,
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Full name",
                "id": "login-username",
            }
        ),
    )
    email = forms.EmailField(
        label="Email (optional)",
        max_length=100,
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "input w-full",
                "Placeholder": "you@gmail.com",
            }
        ),
    )
    address = forms.CharField(
        label="Address line 1",
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "Placeholder": "Main street 1234",
            }
        ),
    )

    address2 = forms.CharField(
        label="Address line 2 (optional)",
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "Placeholder": "Main street 1234",
            }
        ),
    )

    country = forms.ChoiceField(
        choices=Countries,
        label="Country",
        widget=forms.Select(
            attrs={
                "class": "select",
                "placeholder": "Select country",
            }
        ),
    )

    state = forms.ChoiceField(
        label="State (optional)",
        required=False,
        choices=STATES,
        widget=forms.Select(
            attrs={
                "class": "select",
                "placeholder": "State",
            }
        ),
    )

    postal_code = forms.CharField(
        label="Postal code (optional)",
        max_length=8,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "xxxxxx",
            }
        ),
    )

    # card details
    currency = forms.CharField(
        label="Currency",
        max_length=3,
        initial="EUR",
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Currency",
            }
        ),
    )

    card_number = forms.CharField(
        label="Card Number",
        max_length=19,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "xxxx xxxx xxxx xxxx",
            }
        ),
    )

    cvv = forms.CharField(
        label="CVV",
        max_length=3,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "xxx",
            }
        ),
    )

    expiry_month = forms.CharField(
        label="Month",
        max_length=2,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-20",
                "placeholder": "MM",
            }
        ),
    )

    expiry_year = forms.CharField(
        label="Year",
        max_length=2,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-20",
                "placeholder": "YY",
            }
        ),
    )

    card_holder_name = forms.CharField(
        label="Holder Name",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input w-full",
                "placeholder": "Full Name",
            }
        ),
    )
