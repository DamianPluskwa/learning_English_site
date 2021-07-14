from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Word, Answer


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

        answers_english = []
        answers_polish = []

        for current_word in words_all:
            answers_english.append(
                Answer(word=current_word, language="english", text=request.POST[current_word.polish_word])
            )
            answers_polish.append(
                Answer(word=current_word, language="polish", text=request.POST[current_word.english_word])
            )

        for answer in answers_english:
            answer.save()
        for answer in answers_polish:
            answer.save()

        print(len(answers_english))

        return render(
            request,
            "learning_app/exercise_answer.html",
            {
                "answers_english": answers_english,
                "answers_polish": answers_polish
            }
        )

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
