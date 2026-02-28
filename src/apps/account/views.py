from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from apps.orders.views import user_orders

from .forms import RegistrationForm, UserAddressForm, UserEditForm
from .models import Address, Customer
from .token import account_activation_token


# Create your views here.
@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/dashboard.html", {"orders": orders})


# account registration view
def account_register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        # retrieve the data from the POST request
        registerForm = RegistrationForm(request.POST)

        # test the retrieved data
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.is_active = False
            user.save()

            # setup email
            current_site = get_current_site(request)
            subject = "Activate Your Account"

            # create message
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            # send email
            # user.email_user(subject=subject, message=message)
            email = EmailMultiAlternatives(subject=subject, to=[user.email])
            email.attach_alternative(message, "text/html")
            email.send()
            return HttpResponse("Registered successfully and activation sent!")
        else:
            return HttpResponseRedirect("Error handler content", status=400)

    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


# account activation
def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:")
    else:
        # if the activation fails
        return render(request, "account/registration/activation_invalid.html")


# edit user details
@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(
        request, "account/dashboard/edit_details.html", {"user_form": user_form}
    )


# delete user view
@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect("account:delete_confirmation")


# addresses
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
        else:
            return HttpResponseRedirect("Error handler content", status=400)
    else:
        address_form = UserAddressForm()
    return render(
        request, "account/dashboard/edit_addresses.html", {"form": address_form}
    )


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(
        request, "account/dashboard/edit_addresses.html", {"form": address_form}
    )


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect(reverse("account:addresses"))


@login_required
def set_default(request, id):
    # remove any other default address from database
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    # update the new default address
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect(reverse("account:addresses"))
