from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# User manager for the User Model
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Must have an email address')

        if not name:
            raise ValueError('Must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.name


class CategoryModel(models.Model):
    cat_name = models.CharField(max_length=255)

    def __str__(self):
        return self.cat_name


class FoodModel(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(CategoryModel, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255)
    size = models.IntegerField(null=True, blank=True)
    price = models.FloatField()
    description = models.TextField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CartModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + "'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    item_total = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, null=True, blank=True)
    shipping_address = models.TextField()
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    is_cooking = models.BooleanField(default=False)
    is_onTheWay = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)


class OrderItem(models.Model):
    food = models.ForeignKey(FoodModel, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.food.price * self.quantity


# Responses from Contact Us form will be saved here
class FeedbackModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
