import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from web_app.forms import *
from web_app.models import *
from web_app.utils import cartItemToOrderItem, sendOrderConfirmationMail


def home_view(request):  # Home Page
    if request.user.is_authenticated:  # If user is logged in
        user = request.user  # Get the user
        cart = CartModel.objects.get_or_create(user=user)[0]  # Get the cart
        cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items

        context = {  # Context
            'user': user,  # User
            'total_cart_items': cart_items.count(),  # Total cart items
        }
        return render(request, 'pages/index.html', context)  # Render the page with the context
    return render(request, 'pages/index.html')  # Render the page withou the context


def menu_view(request):  # Menu Page
    categories = CategoryModel.objects.all()  # Get all the categories
    all_foods = FoodModel.objects.filter(is_available=True)  # Get all the foods
    classic_pizza = [food for food in all_foods if
                     food.category.cat_name == 'Classic Pizza']  # Get all the foods in the category 'classic pizza'
    gourmet_pizza = [food for food in all_foods if
                     food.category.cat_name == 'Gourmet Pizza']  # Get all the foods in the category 'gourmet pizza'
    burger = [food for food in all_foods if
              food.category.cat_name == 'Burger']  # Get all the foods in the category 'burger'
    pasta = [food for food in all_foods if
             food.category.cat_name == 'Pasta']  # Get all the foods in the category 'pasta'
    sliders = [food for food in all_foods if
               food.category.cat_name == 'Sliders']  # Get all the foods in the category 'sliders'
    set_menu = [food for food in all_foods if
                food.category.cat_name == 'Set Menu']  # Get all the foods in the category 'set menu'
    family_combo = [food for food in all_foods if
                    food.category.cat_name == 'Family Combo Meal']  # Get all the foods in the category 'family combo meal'

    total_cart_items = 0  # Total cart items
    if request.user.is_authenticated:  # If user is logged in
        cart = CartModel.objects.get(user=request.user)  # Get the cart
        cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items
        total_cart_items = cart_items.count()  # Total cart items

    if request.GET.get('AddToCart'):  # If the user clicked the add to cart button
        item_id = int(request.GET.get('foodID'))  # Get the food id
        food_item = FoodModel.objects.get(id=item_id)  # Get the food item
        print(total_cart_items)  # Print the total cart items
        if total_cart_items == 0:  # If the total cart items is 0
            CartItem.objects.create(cart=cart, food=food_item, quantity=1,
                                    item_total=food_item.price)  # Create a cart item
        else:  # If the total cart items is not 0
            for item in cart_items:  # For each cart item
                if item.food.name == food_item.name:  # If the cart item name is the same as the food item name
                    item.quantity += 1  # Increase the quantity
                    item.item_total = item.quantity * item.food.price  # Set the item total
                    item.save()  # Save the cart item
                    return redirect('menu')  # Redirect to the menu page

            CartItem.objects.create(cart=cart, food=food_item, quantity=1,
                                    item_total=food_item.price)  # Create a cart item if the cart item name is not the same as the food item name

        return redirect('menu')  # Redirect to the menu page

    context = {  # Context for the menu page
        'total_cart_items': total_cart_items,  # Total cart items
        'categories': categories,  # Categories list
        'all_foods': all_foods,  # All foods list
        'classic_pizza': classic_pizza,  # Classic pizza list (foods in the category 'classic pizza')
        'gourmet_pizza': gourmet_pizza,  # Gourmet pizza list (foods in the category 'gourmet pizza')
        'burger': burger,  # Burger list (foods in the category 'burger')
        'pasta': pasta,  # Pasta list (foods in the category 'pasta')
        'sliders': sliders,  # Sliders list (foods in the category 'sliders')
        'set_menu': set_menu,  # Set menu list (foods in the category 'set menu')
        'family_combo': family_combo,  # Family combo meal list (foods in the category 'family combo meal')
    }
    return render(request, "pages/menu.html", context)  # Render the page with the context


def food_details_view(request, slug):  # Food Details Page
    food = FoodModel.objects.get(slug=slug)  # Get the food item

    total_cart_items = 0  # Total cart items
    if request.user.is_authenticated:  # If user is logged in
        cart = CartModel.objects.get(user=request.user)  # Get the cart
        cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items
        total_cart_items = cart_items.count()  # Total cart items

    if request.GET.get('AddToCart'):  # If the user clicked the add to cart button
        item_id = int(request.GET.get('foodID'))  # Get the food id
        food_item = FoodModel.objects.get(id=item_id)  # Get the food item
        print(total_cart_items)  # Print the total cart items
        if total_cart_items == 0:  # If the total cart items is 0
            CartItem.objects.create(cart=cart, food=food_item, quantity=1,
                                    item_total=food_item.price)  # Create a cart item
        else:  # If the total cart items is not 0
            for item in cart_items:  # For each cart item
                if item.food.name == food_item.name:  # If the cart item name is the same as the food item name
                    item.quantity += 1  # Increase the quantity
                    item.item_total = item.quantity * item.food.price  # Set the item total
                    item.save()  # Save the cart item
                    return redirect('details', slug)  # Redirect to the food details page

            CartItem.objects.create(cart=cart, food=food_item, quantity=1,
                                    item_total=food_item.price)  # Create a cart item if the cart item name is not the same as the food item name

        return redirect('details', food.slug)  # Redirect to the food details page

    context = {  # Context for the food details page
        'total_cart_items': total_cart_items,  # Total cart items
        'food': food,  # Food item object
    }
    return render(request, "pages/food-details.html", context)  # Render the page with the context


@login_required(login_url='login')  # If user is not logged in redirect to the login page
def cart_view(request):  # Cart Page
    cart = CartModel.objects.get(user=request.user)  # Get the cart
    cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items
    total_cart_items = cart_items.count()  # Total cart items
    total = 0  # Total amount
    for item in cart_items:  # For each cart item
        total += item.food.price * item.quantity  # Add the item total to the total amount

    context = {  # Context for the cart page
        'total_cart_items': total_cart_items,  # Total cart items
        'total': total,  # Total amount
        'cart_items': cart_items,  # Cart items list
    }
    return render(request, "pages/cart.html", context)  # Render the page with the context


@csrf_exempt  # this is to allow the ajax request to be processed
def updateItem(request):  # Update Item Ajax Request
    data = json.loads(request.body)  # Get the data from the ajax request
    foodID = data['foodID']  # Get the food id
    action = data['action']  # Get the action
    print('Product: ', foodID)  # Print the food id
    print('Action: ', action)  # Print the action

    user = request.user  # Get the logged in user
    food = FoodModel.objects.get(id=foodID)  # Get the food item
    cart = CartModel.objects.get(user=user)  # Get the cart
    cart_item = CartItem.objects.get(cart=cart, food=food)  # Get the cart item for the food item

    if action == 'add':  # If the action is add
        cart_item.quantity = (cart_item.quantity + 1)  # Increase the quantity
    elif action == 'remove':  # If the action is remove
        cart_item.quantity = (cart_item.quantity - 1)  # Decrease the quantity

    cart_item.item_total = cart_item.quantity * food.price  # Set the item total to the quantity times the food price
    cart_item.save()  # Save the cart item

    if cart_item.quantity <= 0:  # If the quantity is 0
        cart_item.delete()  # Delete the cart item

    return JsonResponse('Item added', safe=False)  # Return the response


@login_required(login_url='login')  # If user is not logged in redirect to the login page
def proceed_order(request):  # Proceed Order Page
    user = request.user  # Get the logged in user
    profile = ProfileModel.objects.get(user=user)  # Get the profile of the logged in user
    cart = CartModel.objects.get(user=request.user)  # Get the cart of the logged in user
    cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items of the logged in user
    total_cart_items = cart_items.count()  # Total cart items
    total = 0  # Total amount
    for item in cart_items:  # For each cart item
        total += item.food.price * item.quantity  # Add the item total to the total amount

    form = OrderForm()  # Create an order form
    if request.method == 'POST':  # If the request method is POST
        form = OrderForm(request.POST)  # Get the form data
        if form.is_valid():  # If the form is valid
            order = form.save(commit=False)  # Save the form data
            order.total_price = total  # Set the total price
            order.user = request.user  # Set the user
            order.save()  # Save the order
            cartItemToOrderItem(order, cart_items)  # Save the cart items to the order items
            # sendOrderConfirmationMail(user, order, cart_items)  # Send the order confirmation mail
            return redirect('confirm-order', order.id)  # Redirect to the confirm order page

    context = {  # Context for the proceed order page
        'total_cart_items': total_cart_items,  # Total cart items
        'total': total,  # Total amount
        'cart_items': cart_items,  # Cart items list
        'form': form,  # Order form
        'profile': profile,  # Profile object
        'grand_total': total + 50  # Grand total amount
    }
    return render(request, "pages/proceed-order.html", context)  # Render the page with the context


@login_required(login_url='login')  # If user is not logged in redirect to the login page
def confirm_order(request, pk):  # Confirm Order Page
    order = OrderModel.objects.get(id=pk)  # Get the order

    context = {  # Context for the confirm order page
        'total_cart_items': 0,  # Total cart items
        'order': order,  # Order object
    }
    return render(request, "pages/confirm-order.html", context)  # Render the page with the context


def order_details(request, pk):  # Order Details Page
    cart = CartModel.objects.get(user=request.user)  # Get the cart of the logged in user
    cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items of the logged in user
    total_cart_items = cart_items.count()  # Total cart items

    order = OrderModel.objects.get(id=pk)  # Get the order
    order_items = OrderItem.objects.filter(order=order)  # Get the order items

    context = {  # Context for the order details page
        'total_cart_items': total_cart_items,  # Total cart items
        'order': order,  # Order object
        'order_items': order_items,  # Order items list
        'grand_total': order.total_price + 50  # Grand total amount
    }
    return render(request, 'pages/order-details.html', context)  # Render the page with the context
