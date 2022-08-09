from django.urls import path
from django.contrib.auth import views as auth_views

from web_app.views import user_views, food_views, util_views, admin_views

urlpatterns = [
    path('', food_views.home_view, name='home'),

    # user login, logout and registration url
    path('account/login', user_views.login_view, name='login'),
    path('logout', user_views.logout_view, name='logout'),
    path('account/registration', user_views.signup_view, name='register'),
    path('profile/<str:slug>', user_views.profile_view, name='profile'),
    path('edit-profile/<str:slug>', user_views.edit_profile, name='edit-profile'),

    path('menu', food_views.menu_view, name='menu'),
    path('food/<str:slug>', food_views.food_details_view, name='details'),
    path('cart/', food_views.cart_view, name='cart'),
    path('update-item/', food_views.updateItem, name="update-item"),
    path('cart/update-item/', food_views.updateItem, name="update-item"),
    path('proceed-order/', food_views.proceed_order, name="proceed-order"),
    path('confirm-order/<str:pk>/', food_views.confirm_order, name="confirm-order"),
    path('order-details/<str:pk>/', food_views.order_details, name="order-details"),

    # utilities
    path('account/account-settings', util_views.account_settings_view, name='account-settings'),
    path('contact-us', util_views.contact_view, name="contact"),
    path('terms-of-service', util_views.terms_view, name="terms"),
    path('privacy-policy', util_views.privacy_view, name="privacy"),
    path('download', util_views.download_pdf_view, name="download-menu"),

    path('reset-password/',
         auth_views.PasswordResetView.as_view(template_name="pages/auth/password-reset.html"),
         name="reset-password"),
    path('reset-password-sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="pages/auth/password-reset-sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="pages/auth/password-reset-form.html"),
         name="password_reset_confirm"),
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="pages/auth/password-reset-done.html"),
         name="password_reset_complete"),

    # admin panel
    path('admin-panel', admin_views.admin_dashboard, name="admin-dashboard"),
    path('admin/logout', admin_views.admin_logout, name="admin-logout"),

    path('admin-panel/foods', admin_views.admin_foods, name="admin-foods"),
    path('admin-panel/add-food', admin_views.admin_add_food, name="admin-add-food"),
    path('admin-panel/edit-food/<str:pk>', admin_views.admin_edit_food, name="admin-edit-food"),
    path('admin-panel/delete-food/<str:pk>', admin_views.admin_delete_food, name="admin-delete-food"),

    path('admin-panel/categories', admin_views.admin_categories, name="admin-categories"),
    path('admin-panel/add-category', admin_views.admin_add_category, name="admin-add-category"),
    path('admin-panel/edit-category/<str:pk>', admin_views.admin_edit_category, name="admin-edit-category"),
    path('admin-panel/delete-category/<str:pk>', admin_views.admin_delete_category, name="admin-delete-category"),

    path('admin-panel/users', admin_views.admin_users, name="admin-users"),
    path('admin-panel/add-user', admin_views.admin_add_user, name="admin-add-user"),
    path('admin-panel/edit-user/<str:pk>', admin_views.admin_edit_user, name="admin-edit-user"),
    path('admin-panel/delete-user/<str:pk>', admin_views.admin_delete_user, name="admin-delete-user"),

    path('admin-panel/orders', admin_views.admin_orders, name="admin-orders"),
    path('admin-panel/update-order/<str:pk>', admin_views.admin_update_order, name="admin-update-order"),
    path('admin-panel/delete-order/<str:pk>', admin_views.admin_delete_order, name="admin-delete-order"),

    path('admin-panel/feedbacks', admin_views.admin_view_feedbacks, name="admin-feedbacks"),
]
