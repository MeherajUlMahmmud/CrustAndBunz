from django.core.mail import send_mail
from django.template import loader
from django.template.loader import get_template

from web_app.models import OrderItem


# def sendVerificationEmail(email, link):
#     subject = "Crust and Bunz : Email Verification"
#     from_email = 'crustnbunz@gmail.com' # The email address of the sender
#     context = { # The context of the email
#         "link": link # The link to the verification page
#     }
#     msg_plain = loader.render_to_string('email-templates/email-verification.txt', context) # The plain text version of the email
#     msg_html = loader.render_to_string('email-templates/email-verification.html', context) # The html version of the email

#     send_mail(subject, msg_plain, from_email, [email], fail_silently=True, html_message=msg_html) # Send the email to the user
#     return True 


def cartItemToOrderItem(order, cart_items): # A function to convert cart items to order items
    for item in cart_items: # For each item in the cart
        OrderItem.objects.create(food=item.food, order=order, quantity=item.quantity) # Create an order item
        item.delete() # Delete the cart item


def sendOrderConfirmationMail(user, order, order_items): # A function to send an email to the user when an order is placed
    subject = "Crust and Bunz : Order Confirmation" # The subject of the email
    from_email = 'crustnbunz@gmail.com' # The email address of the sender

    order_link = "http://127.0.0.1:8000" # The link to the order page
    context = { # The context of the email
        "user": user, # The user who placed the order
        "order": order, # The order object
        "order_items": order_items, # The order items of the order
        "order_link": order_link, # The link to the order page
        "grand_total": order.total_price + 50 # The grand total of the order
    }
    msg_plain = loader.render_to_string('email-templates/order-confirmation.txt', context) # The plain text version of the email
    msg_html = loader.render_to_string('email-templates/order-confirmation.html', context) # The html version of the email

    send_mail(subject, msg_plain, from_email, [user.email], fail_silently=True, html_message=msg_html) # Send the email to the user
    return True 
