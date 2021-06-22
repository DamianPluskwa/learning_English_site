from django.shortcuts import render


def menu(request):
    return render(
        request,
        "learning_app/menu.html",
        {}
    )
