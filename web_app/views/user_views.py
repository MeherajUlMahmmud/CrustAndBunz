from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from web_app.forms import RegistrationForm, LoginForm, EditProfileForm
from web_app.models import CartModel, CartItem, UserModel, ProfileModel, OrderModel

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.text import slugify

from web_app.decorators import unauthenticated_user


@unauthenticated_user  # this decorator is used to prevent logged in users from accessing the login page
def login_view(request):  # login view
    if request.POST:  # if the request is a post request
        form = LoginForm(request.POST)  # create a form object with the data from the request
        if form.is_valid():  # if the form is valid
            email = request.POST['email']  # get the email from the request
            password = request.POST['password']  # get the password from the request
            user = authenticate(email=email, password=password)  # authenticate the user

            if user and user.is_admin:  # if the user is an admin
                login(request, user)  # login the user
                return redirect('admin-dashboard')  # redirect to the admin dashboard

            elif user and user.is_active:  # if the user is active
                login(request, user)  # login the user
                if request.GET.get('next'):  # if there is a next parameter in the request
                    return redirect(request.GET.get('next'))  # redirect to the next parameter
                return redirect('home')  # redirect to the home page

            elif user and not user.is_active:  # if the user is not active
                messages.error(request, 'Account is deactivated')  # display an error message
                return redirect('login')  # redirect to the login page

            else:  # if the user is not authenticated
                messages.error(request, 'Email or Password is incorrect.')  # display an error message
                return redirect('login')  # redirect to the login page
        else:  # if the form is not valid
            return render(request, 'pages/auth/login.html', {'form': form})  # render the login page with the form

    else:  # if the request is not a post request
        form = LoginForm()  # create a form object

    context = {  # context for the login page
        'form': form  # form object
    }
    return render(request, 'pages/auth/login.html', context)  # render the login page with the form object


def logout_view(request):  # logout view
    logout(request)  # logout the user
    return redirect('login')  # redirect to the login page


@unauthenticated_user  # this decorator is used to prevent logged in users from accessing the register page
def signup_view(request):  # signup view
    if request.method == "POST":  # if the request is a post request
        form = RegistrationForm(request.POST)  # create a form object with the data from the request
        if form.is_valid():  # if the form is valid
            form.save()  # save the form
            email = request.POST['email']  # get the email from the request
            password = request.POST['password1']  # get the password from the request
            user = authenticate(request, email=email, password=password)  # authenticate the user
            slug_str = "%s %s" % (user.name, user.id)  # create a slug string
            user.slug = slugify(slug_str)  # assign the slug to the user
            token, created = Token.objects.get_or_create(user=user) # create a token for the user
            user.token = token.key # assign the token to the user
            user.save()  # save the user
            ProfileModel.objects.create(user=user)  # create a profile for the user
            CartModel.objects.create(user=user)  # create a cart for the user
            login(request, user)  # login the user
            return redirect('home')  # redirect to the home page
        else:  # if the form is not valid
            form = RegistrationForm()  # create a form object
            context = {  # context for the signup page
                'form': form  # form object
            }
            return render(request, 'pages/auth/sign-up.html', context)  # render the signup page with the form object

    else:  # if the request is not a post request
        form = RegistrationForm()  # create a form object

    context = {  # context for the signup page
        'form': form  # form object
    }
    return render(request, 'pages/auth/sign-up.html', context)


@login_required(
    login_url='login')  # this decorator is used to prevent unauthenticated users from accessing the profile page
def profile_view(request, slug):  # profile view
    if request.user.is_admin:  # if the user is an admin
        # redirect to the admin dashboard
        return redirect('admin-dashboard')
    
    cart = CartModel.objects.get(user=request.user)  # get the cart for the user
    cart_items = CartItem.objects.filter(cart=cart)  # get the cart items for the cart
    orders = OrderModel.objects.filter(user=request.user).order_by(
        '-date_ordered')  # get the orders for the user ordered by date_ordered attribute in descending order

    is_self = False  # is_self is a boolean variable that is used to determine if the user is viewing his/her own profile

    user = UserModel.objects.get(slug=slug)  # get the user for the slug
    if request.user == user:  # if the user is viewing his/her own profile
        is_self = True  # set is_self to true

    profile = ProfileModel.objects.get(user=user)  # get the profile for the user

    context = {  # context for the profile page
        'total_cart_items': cart_items.count(),  # total cart items
        'user': user,  # user
        'is_self': is_self,  # is_self
        'profile': profile,  # profile
        'orders': orders,  # orders
    }
    return render(request, "pages/profile.html", context)  # render the profile page with the context


@login_required(
    login_url='login')  # this decorator is used to prevent unauthenticated users from accessing the profile page
def edit_profile(request, slug):  # edit profile view
    cart = CartModel.objects.get(user=request.user)  # get the cart for the user
    cart_items = CartItem.objects.filter(cart=cart)  # get the cart items for the cart
    user = UserModel.objects.get(slug=slug)  # get the user for the slug
    profile = ProfileModel.objects.get(user=request.user)  # get the profile for the user

    form = EditProfileForm(instance=profile)  # create a form object with the profile instance
    if request.method == 'POST':  # if the request is a post request
        form = EditProfileForm(request.POST, request.FILES,
                               instance=profile)  # create a form object with the data from the request and the profile instance
        if form.is_valid():  # if the form is valid
            form.save()  # save the form
            return redirect('profile', request.user.slug)  # redirect to the profile page for the user
        else:  # if the form is not valid
            return redirect('edit-profile')  # redirect to the edit profile page

    context = {  # context for the edit profile page
        'total_cart_items': cart_items.count(),  # total cart items
        'user': user,  # user
        'form': form,  # form
        'profile': profile,  # profile
    }
    return render(request, 'pages/edit-profile.html', context)  # render the edit profile page with the context
