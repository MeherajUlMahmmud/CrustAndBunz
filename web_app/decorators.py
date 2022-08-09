from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func): # this is a decorator function that is used to check if the user is authenticated or not
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated: # if the user is authenticated then it will redirect to the home page
            return redirect('home')
        else: # if the user is not authenticated then it will execute the view function
            return view_func(request, *args, **kwargs)

    return wrapper_func 


def show_to_admin(allowed_roles=[]): # this is a decorator function that is used to allow the user to see the page only if the user is an admin
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs): 
            if request.user.is_admin: # if the user is an admin then it will execute the view function
                return view_func(request, *args, **kwargs)
            else: # if the user is not an admin then it will show the error page
                return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator
