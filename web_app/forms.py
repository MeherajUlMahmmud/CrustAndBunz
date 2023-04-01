from django import forms
from django.contrib.auth.forms import UserCreationForm, authenticate
from django.forms import ModelForm

from .models import *


class LoginForm(forms.Form):  # Inherits from forms.Form class
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def clean(self):  # This method is called when the form is submitted
        if self.is_valid():  # If the form is valid
            email = self.cleaned_data.get('email')  # Get the email from the form data
            password = self.cleaned_data.get('password')  # Get the password from the form data
            if not authenticate(email=email, password=password):  # If the user is not authenticated
                raise forms.ValidationError("Invalid Username or Password")  # Raise an error


class RegistrationForm(UserCreationForm):  # Inherits from the UserCreationForm class
    email = forms.EmailField(max_length=255, help_text='Required. Add a valid email address',
                             widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))  # Add an email field
    name = forms.CharField(max_length=60,
                           widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))  # Add a name field
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text='Password must contain at least 8 character including numeric values',
    )  # Add a password field
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text='Re-type Password',
    )  # Add a password confirmation field
    check = forms.BooleanField(required=True)  # Add a checkbox field

    class Meta:
        model = UserModel  # Set the model to the UserModel
        fields = ("name", "email", "password1", "password2", "check")  # Set the fields to the above fields


class EditProfileForm(ModelForm):  # a form to edit the user profile
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )  # Add an image field

    class Meta:
        model = ProfileModel  # Set the model to the ProfileModel
        fields = '__all__'  # Set the fields to all the fields in the ProfileModel
        exclude = ['user']  # Exclude the user field from the form


class OrderForm(ModelForm):  # a form to create an order
    PAYMENT_METHOD_CHOICES = [  # A list of payment methods
        ('', 'Payment Method'),
        ('Cash on Delivery', 'Cash on Delivery'),
        ('bKash', 'bKash'),
        ('Nagad', 'Nagad'),
    ]

    payment_method = forms.CharField(widget=forms.Select(choices=PAYMENT_METHOD_CHOICES))  # Add a payment method field

    class Meta:
        model = OrderModel  # Set the model to the OrderModel
        fields = ['payment_method', 'phone', 'transaction_id', 'shipping_address']  # Set the fields to the above fields


class AccountInformationForm(ModelForm):  # a form to edit the user account information
    class Meta:
        model = UserModel  # Set the model to the UserModel
        fields = ('name', 'email')  # Set the fields to the above fields


class AddEditFoodForm(ModelForm):  # a form to add or edit a food item
    image = forms.ImageField(
        required=True,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput,
    )  # Add an image field

    class Meta:
        model = FoodModel  # Set the model to the FoodModel
        fields = '__all__'  # Set the fields to all the fields in the FoodModel
        exclude = ['slug']  # Exclude the slug field from the form


class AddEditCategoryForm(ModelForm):  # a form to add or edit a category
    class Meta:
        model = CategoryModel  # Set the model to the CategoryModel
        fields = '__all__'  # Set the fields to all the fields in the CategoryModel


class AddEditUserForm(ModelForm):  # a form to add or edit a user
    class Meta:
        model = UserModel  # Set the model to the UserModel
        fields = ['email', 'name', 'is_active', 'is_admin']  # Set the fields to the above fields


class UpdateOrderForm(ModelForm):  # a form to update an order
    class Meta:
        model = OrderModel  # Set the model to the OrderModel
        fields = ['shipping_address', 'is_pending', 'is_confirmed', 'is_cooking', 'is_onTheWay',
                  'is_delivered']  # Set the fields to the above fields
