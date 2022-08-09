from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

from api.views import user_views, food_views

urlpatterns = [
    path('all_foods/', food_views.get_all_foods),
    path('food_by_id/<str:food_id>/', food_views.get_food_by_id),
    path('foods_by_category/<str:category>/',
         food_views.get_foods_by_category),

    # user login, logout and registration url
    path('login/', user_views.login_view),
    path('registration/', user_views.signup_view),

    # profile and update profile url
    path('profile/', user_views.profile_view),
    path('update_user/', user_views.update_user),
    path('update_profile/', user_views.update_profile),
    path('update_profile_image/', user_views.update_profile_image),

    # food urls
    path('add_to_cart/', food_views.add_to_cart),
    path('get_total_cart_items/', food_views.get_total_cart_items),
    path('get_cart_items/', food_views.get_cart_items),
    path('increase_item_quantity/<str:cart_item_id>/',
         food_views.increase_quantity),
    path('decrease_item_quantity/<str:cart_item_id>/',
         food_views.decrease_quantity),
    path('remove_from_cart/<str:cart_item_id>/',
         food_views.remove_from_cart),

         
    path('get_orders_by_user/', food_views.get_orders_by_user),
    path('get_orders_by_id/<str:pk>/', food_views.get_orders_by_id),
    path('get_order_items/<str:pk>/', food_views.get_order_items),
    path('get_foods_by_order/<str:pk>/', food_views.get_foods_by_order),
    path('place_order/', food_views.place_order),

    # util
    path('feedback/', user_views.feedback_view),
    path('update_password/', user_views.update_password),
]
