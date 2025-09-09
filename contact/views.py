
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings

def contact_view(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]

            # Email body
            full_message = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ["ayeshaa00132@gmail.com"],  # Abhi tumhara Gmail, baad me client ka dal dena
                fail_silently=False,
            )

            success = True
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form, "success": success})
