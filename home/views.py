from django.shortcuts import render


def home(request):
    context = {
        "name": "Dnyaneshwar",
        "course": "Django",
        "message": "Welcome to my first Django website!"
    }

    return render(request, "home/index.html", context)