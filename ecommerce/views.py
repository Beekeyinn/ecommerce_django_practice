
from django.shortcuts import redirect, render
from .forms import Contact_Form
def homepage(request):
    context =  {
        'title':"HomePage",
        'content':"Welcome to Home Page."
    }
    if request.user.is_authenticated:
        context['logger'] = "You are logged in."
    return render(request, "homepage.html",context)

def about_page(request):
    context =  {
        'title':"About",
        'content':"Welcome to About Page."
    }
    return render(request, "homepage.html",context)

def contact_page(request):
    form = Contact_Form(request.POST or None)
    context =  {
        'title':"Contact",
        'content':"Welcome to Contact Page.",
        'form':form
    }

    if form.is_valid():
        print(form.cleaned_data)

    return render(request, "contact/contact.html",context)

