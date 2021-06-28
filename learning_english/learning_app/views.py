from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

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


def detail(request, word_id):
    word = get_object_or_404(Word, pk=word_id)

    return render(
        request,
        "learning_app/detail.html",
        {"word": word}
    )


def exercise(request):
    if request.method == 'POST':
        words_all = (Word.objects.get(id=1), Word.objects.get(id=2))

        print('-'*20)
        print('wysłane', request.POST)
        print('-' * 20)

        form = request.POST['text']
        print(form)
        print('-' * 20)
        form = request.POST['text']
        print(form)
        print('-' * 20)
        answer_1 = request.POST[words_all[0].english_word]
        print(answer_1)
        print('-' * 20)

    else:
        # words_all = Word.objects.all()

        words_all = (Word.objects.get(id=1), Word.objects.get(id=2))

    return render(
        request,
        "learning_app/exercise.html",
        {
            "words": words_all
        }
    )
