from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Word


def menu(request):
    return render(
        request,
        "learning_app/menu.html",
        {}
    )


def word_list(request):
    words_all = Word.objects.all()

    paginator = Paginator(words_all, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "learning_app/word_list.html",
        {"page_obj": page_obj}
    )
