import os

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import slugify

from base import settings
from web_app.forms import AccountInformationForm
from web_app.models import CartItem, CartModel, FeedbackModel


@login_required(login_url='login')  # redirects to login page if user is not logged in
def account_settings_view(request):  # user must be logged in to access this view
    user = request.user  # get the user
    cart = CartModel.objects.get(user=user)  # get the user's cart
    cart_items = CartItem.objects.filter(cart=cart)  # get the cart items
    total_cart_items = cart_items.count()  # get the total number of cart items

    information_form = AccountInformationForm(instance=user)  # create an instance of the AccountInformationForm
    password_form = PasswordChangeForm(request.user)  # create an instance of the PasswordChangeForm
    if request.method == 'POST':  # if the request method is POST
        information_form = AccountInformationForm(request.POST,
                                                  instance=user)  # create an instance of the AccountInformationForm with the POST data
        password_form = PasswordChangeForm(request.user,
                                           request.POST)  # create an instance of the PasswordChangeForm with the POST data

        if information_form.is_valid():  # if the AccountInformationForm is valid
            information_form.save()  # save the AccountInformationForm
            slug_str = "%s %s" % (user.name, user.id)  # create a string to be used as the slug
            user.slug = slugify(slug_str)  # set the user's slug to the slugified string
            user.save()  # save the user
            return redirect('account-settings')  # redirect to the account settings view

        elif password_form.is_valid():  # if the PasswordChangeForm is valid
            user = password_form.save()  # save the PasswordChangeForm
            update_session_auth_hash(request,
                                     user)  # Important! Otherwise we will get "changed password" error on the login page
            messages.success(request, 'Your password was successfully updated!')  # display a success message
            return redirect('account-settings')  # redirect to the account settings view
        else:  # if the AccountInformationForm or PasswordChangeForm is invalid
            context = {  # create a context
                'total_cart_items': total_cart_items,  # add the total number of cart items to the context
                'information_form': information_form,  # add the AccountInformationForm to the context
                'password_form': password_form,  # add the PasswordChangeForm to the context
            }
            return render(request, 'pages/account-settings.html',
                          context)  # render the account settings view with the context
    context = {  # create a context
        'total_cart_items': total_cart_items,  # add the total number of cart items to the context
        'information_form': information_form,  # add the AccountInformationForm to the context
        'password_form': password_form,  # add the PasswordChangeForm to the context
    }
    return render(request, 'pages/utils/settings.html', context)  # render the account settings view with the context


def contact_view(request):  # contact view
    if request.user.is_authenticated:  # if the user is logged in
        user = request.user  # get the user
        cart = CartModel.objects.get(user=user)  # get the user's cart
        cart_items = CartItem.objects.filter(cart=cart)  # get the cart items
        total_cart_items = cart_items.count()  # get the total number of cart items

        if request.method == 'POST':  # if the request method is POST
            name = request.POST['name']  # get the name from the POST data
            email = request.POST['email']  # get the email from the POST data
            subject = request.POST['subject']  # get the subject from the POST data
            message = request.POST['message']  # get the message from the POST data
            FeedbackModel.objects.create(name=name, email=email, subject=subject,
                                         message=message)  # create a new Feedback

            messages.success(request, "Feedback sent successfully.")  # display a success message
        context = {  # create a context
            'total_cart_items': total_cart_items  # add the total number of cart items to the context
        }
        return render(request, 'pages/utils/contact.html', context)  # render the contact view with the context

    return render(request, 'pages/utils/contact.html', )  # render the contact view without the context


def terms_view(request):  # terms and conditions view
    return render(request, 'pages/utils/terms-of-service.html')  # render the terms and conditions view


def privacy_view(request):  # privacy policy view
    return render(request, 'pages/utils/privacy-policy.html')  # render the privacy policy view


def download_pdf_view(request):  # download pdf view
    with open(os.path.join(settings.STATICFILES_DIRS[0], 'CrustnBunz_Menu.pdf'), 'rb') as fh:  # open the pdf file
        response = HttpResponse(fh.read(), content_type="application/pdf")  # create a response with the pdf file
        response[
            'Content-Disposition'] = 'attachment; filename=CrustnBunz_Menu.pdf'  # set the content disposition to download the pdf file
        return response
