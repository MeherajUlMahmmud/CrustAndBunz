from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.text import slugify

from web_app.decorators import show_to_admin
from web_app.forms import AddEditUserForm, AddEditCategoryForm, AddEditFoodForm, UpdateOrderForm
from web_app.models import *


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    elif request.user.is_authenticated and request.user.is_admin:
        categories = CategoryModel.objects.all()
        foods = FoodModel.objects.all()
        users = ProfileModel.objects.all()
        pending_orders = OrderModel.objects.filter(is_pending=True)
        cooking_orders = OrderModel.objects.filter(is_cooking=True)
        context = {
            'total_categories': categories.count(),
            'total_food_item': foods.count(),
            'total_users': users.count(),
            'total_pending_orders': pending_orders.count(),
            'pending_orders': pending_orders,
            'cooking_orders': cooking_orders,
        }

        return render(request, 'admin-panel/dashboard.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_logout(request):
    logout(request)
    redirect('home')


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_foods(request):
    foods = FoodModel.objects.all()
    context = {
        'foods': foods,
    }
    return render(request, 'admin-panel/food/foods.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_add_food(request):
    task = "Add New"
    form = AddEditFoodForm()
    categories = CategoryModel.objects.all()

    if request.method == 'POST':
        form = AddEditFoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)

            if food.size:
                slug_str = "%s %s", (food.name, food.size)
            else:
                slug_str = food.name

            food.slug = slugify(slug_str)
            food.save()
            return redirect('admin-foods')
        else:
            context = {
                'task': task,
                'form': form,
                'categories': categories,
            }
            return render(request, 'admin-panel/food/add-edit-food.html', context)

    context = {
        'task': task,
        'form': form,
        'categories': categories,
    }
    return render(request, 'admin-panel/food/add-edit-food.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_edit_food(request, pk):
    task = "Update"
    food = FoodModel.objects.get(id=pk)

    form = AddEditFoodForm(instance=food)
    if request.method == 'POST':
        form = AddEditFoodForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('admin-foods')
        else:
            context = {
                'food': food,
                'task': task,
                'form': form,
            }
            return render(request, 'admin-panel/food/add-edit-food.html', context)

    context = {
        'food': food,
        'task': task,
        'form': form,
    }
    return render(request, 'admin-panel/food/add-edit-food.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_delete_food(request, pk):
    task = "Delete"
    food = FoodModel.objects.get(id=id)

    if request.method == 'POST':
        food.delete()
        return redirect('admin-foods')
    context = {
        'food': food,
        'task': task,
    }
    return render(request, 'admin-panel/food/delete-food.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_categories(request):
    categories = CategoryModel.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'admin-panel/category/categories.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_add_category(request):
    task = "Add New"
    form = AddEditCategoryForm()

    if request.method == 'POST':
        form = AddEditCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-categories')
        else:
            context = {
                'task': task,
                'form': form,
            }
            return render(request, 'admin-panel/category/add-edit-category.html', context)

    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'admin-panel/category/add-edit-category.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_edit_category(request, pk):
    task = "Update"
    category = CategoryModel.objects.get(id=pk)

    form = AddEditCategoryForm(instance=category)
    if request.method == 'POST':
        form = AddEditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin-categories')
        else:
            context = {
                'category': category,
                'task': task,
                'form': form,
            }
            return render(request, 'admin-panel/category/add-edit-category.html', context)

    context = {
        'category': category,
        'task': task,
        'form': form,
    }
    return render(request, 'admin-panel/category/add-edit-category.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_delete_category(request, pk):
    task = "Delete"
    category = CategoryModel.objects.get(id=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('admin-categories')
    context = {
        'category': category,
        'task': task,
    }
    return render(request, 'admin-panel/category/delete-category.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_orders(request):
    orders = OrderModel.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'admin-panel/order/orders.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_update_order(request, pk):
    task = 'Update'
    order = OrderModel.objects.get(id=pk)
    order_items = OrderItem.objects.filter(order=order)

    form = UpdateOrderForm(instance=order)
    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('admin-orders')
        else:
            print(form)
            context = {
                'order': order,
                'order_items': order_items,
                'task': task,
                'form': form,
            }
            return render(request, 'admin-panel/order/update-order.html', context)

    context = {
        'order': order,
        'order_items': order_items,
        'task': task,
        'form': form,
    }
    return render(request, 'admin-panel/order/update-order.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_delete_order(request, pk):
    task = "Delete"
    order = OrderModel.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('admin-orders')
    context = {
        'order': order,
        'task': task,
    }
    return render(request, 'admin-panel/order/delete-order.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_users(request):
    users = UserModel.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin-panel/user/users.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_add_user(request):
    task = "Add New"
    form = AddEditUserForm()

    if request.method == 'POST':
        form = AddEditUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-users')
        else:
            context = {
                'task': task,
                'form': form,
            }
            return render(request, 'admin-panel/user/add-edit-user.html', context)

    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'admin-panel/user/add-edit-user.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_edit_user(request, pk):
    task = "Update"
    user = UserModel.objects.get(id=pk)

    form = AddEditUserForm(instance=user)
    if request.method == 'POST':
        form = AddEditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin-users')
        else:
            context = {
                'user': user,
                'task': task,
                'form': form,
            }
            return render(request, 'admin-panel/user/add-edit-user.html', context)

    context = {
        'user': user,
        'task': task,
        'form': form,
    }
    return render(request, 'admin-panel/user/add-edit-user.html', context)


@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_delete_user(request, pk):
    task = "Update"
    user = UserModel.objects.get(id=pk)

    if request.method == 'POST':
        user.delete()
        return redirect('admin-users')
    context = {
        'user': user,
        'task': task,
    }
    return render(request, 'admin-panel/user/delete-user.html', context)



@login_required(login_url='login')
@show_to_admin(allowed_roles=['is_admin'])
def admin_view_feedbacks(request):
    feedbacks = FeedbackModel.objects.all()

    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'admin-panel/feedback/all-feedbacks.html', context)
