# import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from api.serializers.food_serializer import *
from api.serializers.user_serializer import *
from web_app.models import *
from web_app.utils import cartItemToOrderItem, sendOrderConfirmationMail


@api_view(['GET'])
def get_all_foods(request):
    foods = FoodModel.objects.filter(is_available=True)
    serialized = FoodModelSerializer(foods, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def get_foods_by_category(request, category):
    foods = FoodModel.objects.filter(
        category__cat_name=category, is_available=True)
    serialized = FoodModelSerializer(foods, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def get_food_by_id(request, food_id):
    food = FoodModel.objects.get(id=food_id, is_available=True)
    serialized = FoodModelSerializer(food, many=False)
    return Response(serialized.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    data = request.data
    user = UserModel.objects.get(id=request.user.id)
    food = FoodModel.objects.get(id=data['food_id'])

    try:
        cart = CartModel.objects.get(user=user)  # Get the cart
        cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items
        total_cart_items = cart_items.count()  # Total cart items

        if total_cart_items == 0:  # If the total cart items is 0
            CartItem.objects.create(
                cart=cart, food=food, quantity=1, item_total=food.price)  # Create a cart item
        else:  # If the total cart items is not 0
            for item in cart_items:  # For each cart item
                if item.food.name == food.name:  # If the cart item name is the same as the food item name
                    item.quantity += 1  # Increase the quantity
                    item.item_total = item.quantity * item.food.price  # Set the item total
                    item.save()  # Save the cart item
                    return Response(status=HTTP_200_OK)

            CartItem.objects.create(
                cart=cart, food=food, quantity=1, item_total=food.price)
            return Response(status=HTTP_200_OK)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_cart_items(request):
    user = UserModel.objects.get(id=request.user.id)
    cart = CartModel.objects.get(user=user)  # Get the cart
    cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items
    return Response({'total_cart_items': cart_items.count()}, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_items(request):
    try:
        user = UserModel.objects.get(id=request.user.id)
        cart = CartModel.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        serialized = CartItemSerializer(cart_items, many=True)
        return Response(serialized.data)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def increase_quantity(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity += 1
        cart_item.item_total = cart_item.quantity * cart_item.food.price
        cart_item.save()
        return Response(status=HTTP_200_OK)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def decrease_quantity(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity -= 1
        cart_item.item_total = cart_item.quantity * cart_item.food.price
        cart_item.save()

        if cart_item.quantity <= 0:
            cart_item.delete()
        return Response(status=HTTP_200_OK)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return Response(status=HTTP_200_OK)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_by_user(request):
    try:
        user = UserModel.objects.get(id=request.user.id)
        orders = OrderModel.objects.filter(user=user)
        serialized = OrderModelSerializer(orders, many=True)
        return Response(serialized.data)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_by_id(request, pk):
    try:
        order = OrderModel.objects.get(id=pk)
        serialized = OrderModelSerializer(order, many=False)
        return Response(serialized.data)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders_items_by_id(request, pk):
    try:
        order = OrderModel.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=order)
        serialized = OrderItemSerializer(order_items, many=True)
        return Response(serialized.data)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_items(request, pk):
    try:
        order = OrderModel.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=order)
        serialized = OrderItemSerializer(order_items, many=True)
        return Response(serialized.data)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_foods_by_order(request, pk):
    try:
        order = OrderModel.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=order)
        foods = []
        for item in order_items:
            food = FoodModel.objects.get(id=item.food.id)
            foods.append(food)
        serialized = FoodModelSerializer(foods, many=True)
        return Response(serialized.data)
    except:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    data = request.data
    payment_method = data['payment_method']
    transaction_id = data['transaction_id']
    phone = data['phone']
    address = data['address']
    # try:
    user = request.user  # Get the logged in user
    cart = CartModel.objects.get(user=request.user)  # Get the cart of the logged in user
    cart_items = CartItem.objects.filter(cart=cart)  # Get the cart items of the logged in user
    total = 0  # Total amount
    for item in cart_items:  # For each cart item
        total += item.food.price * item.quantity  # Add the item total to the total amount
    order = OrderModel.objects.create(
        user=user,
        total_price=total,
        transaction_id=transaction_id,
        payment_method=payment_method,
        phone=phone,
        shipping_address=address)
    
    cartItemToOrderItem(order, cart_items)  # Save the cart items to the order items
    sendOrderConfirmationMail(user, order, cart_items)  # Send the order confirmation mail
    serialized_data = OrderModelSerializer(order, many=False).data
    return Response(serialized_data, status=HTTP_200_OK)
    # except:
    #     return Response(status=HTTP_404_NOT_FOUND)
