from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .forms import WordForm
from .models import Word, Answer


class WordModelTests(TestCase):

    def test_create_instance_of_word(self):
        word = Word(english_word='english', polish_word='angielski')
        self.assertIsInstance(word, Word)

    def test_str_method(self):
        word = Word(english_word='english', polish_word='angielski')
        self.assertEqual(str(word), 'english 1 - 1 angielski')

    def test_all_attributes(self):
        word = Word(english_word='english', polish_word='angielski')
        self.assertEqual(word.english_word, 'english')
        self.assertEqual(word.polish_word, 'angielski')
        self.assertEqual(word.level_of_knowledge_english, 1)
        self.assertEqual(word.level_of_knowledge_polish, 1)


class AnswerModelTests(TestCase):

    def test_create_instance_of_answer(self):
        word = Word(english_word='english', polish_word='angielski')
        answer = Answer(word=word, language='english', text='english')
        self.assertIsInstance(answer, Answer)

    def test_str_method(self):
        word = Word(english_word='english', polish_word='angielski')
        answer = Answer(word=word, language='english', text='english')
        self.assertEqual(str(answer), f"{word} english english None True")

    def test_every_attribute(self):
        word = Word(english_word='english', polish_word='angielski')
        time = timezone.now()
        answer = Answer(word=word, language='english', text='english', date=time)
        self.assertEqual(answer.word, word)
        self.assertEqual(answer.language, 'english')
        self.assertEqual(answer.text, 'english')
        self.assertEqual(answer.date, time)

    def test_property_true(self):
        word = Word(english_word='english', polish_word='angielski')
        answer = Answer(word=word, language='english', text='english')
        self.assertIs(answer.is_correct, True)

    def test_property_false(self):
        word = Word(english_word='english', polish_word='angielski')
        answer_1 = Answer(word=word, language='english', text='wrong')
        answer_2 = Answer(word=word, language='english', text='')
        self.assertIs(answer_1.is_correct, False)
        self.assertIs(answer_2.is_correct, False)

    def test_property_wrong_language(self):
        word = Word(english_word='english', polish_word='angielski')
        answer = Answer(word=word, language='', text='english')
        with self.assertRaises(ValueError):
            a = answer.is_correct


class MenuViewTest(TestCase):

    def test_menu_contains(self):
        response = self.client.get(reverse('learning_app:menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menu")
        self.assertContains(response, "Lista wyrazów")
        self.assertContains(response, "Zadania")
        self.assertContains(response, "Wprowadzenie nowego wyrazu")


class WordListViewTest(TestCase):

    def test_no_words(self):
        response = self.client.get(reverse('learning_app:word_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brak wyrazów w słowniku')
        self.assertQuerysetEqual(response.context['page_obj'], [])

    def test_one_word(self):
        word = Word.objects.create(english_word='english', polish_word='angielski')
        response = self.client.get(reverse('learning_app:word_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['page_obj'],
            [word]
        )

    def test_more_then_twenty_words(self):
        for _ in range(21):
            Word.objects.create(english_word='english', polish_word='angielski')
        response = self.client.get(reverse('learning_app:word_list'))
        self.assertEqual(
            len(response.context['page_obj']),
            20
        )


class DetailViewTest(TestCase):

    def test_correct_id(self):
        word = Word.objects.create(english_word='english', polish_word='angielski')
        url = reverse('learning_app:detail', args=(word.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['word'], word)
        self.assertContains(response, "english")
        self.assertContains(response, "angielski")
        self.assertContains(response, "Menu")

    def test_incorrect_id(self):
        url = reverse('learning_app:detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ExerciseViewTest(TestCase):
    def test_no_words(self):
        response = self.client.get(reverse('learning_app:exercise'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brak zadań na dzisiaj')
        self.assertQuerysetEqual(response.context['words'], [])

    def test_one_word(self):
        word = Word.objects.create(english_word='english', polish_word='angielski')
        response = self.client.get(reverse('learning_app:exercise'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'english')
        self.assertContains(response, 'angielski')
        self.assertQuerysetEqual(response.context['words'], [word])

    def test_one_word_answer(self):
        word = Word.objects.create(english_word='english', polish_word='angielski')
        response = self.client.post("/exercise/", {'angielski': 'english', 'english': 'angielski'})
        time = timezone.now()

        answer_all = Answer.objects.all()

        self.assertIs(len(answer_all), 2)

        self.assertEqual(answer_all[0].word, word)
        self.assertEqual(answer_all[0].language, 'english')
        self.assertEqual(answer_all[0].text, 'english')
        self.assertIs(answer_all[0].date <= time, True)
        self.assertIs(answer_all[0].date + timedelta(minutes=1) >= time, True)

        self.assertEqual(answer_all[1].word, word)
        self.assertEqual(answer_all[1].language, 'polish')
        self.assertEqual(answer_all[1].text, 'angielski')
        self.assertIs(answer_all[1].date <= time, True)
        self.assertIs(answer_all[1].date + timedelta(minutes=1) >= time, True)


class WordFormTest(TestCase):
    def test_create_instance_of_word_form(self):
        form = WordForm()
        self.assertIsInstance(form, WordForm)

    def test_valid_data(self):
        form_data = {'english_word': 'english', 'polish_word': 'angielski'}
        form = WordForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['english_word'], 'english')
        self.assertEqual(form.cleaned_data['polish_word'], 'angielski')

    def test_unvalid_data(self):
        form_data1 = {'english_word': 'english'}
        form_data2 = {'polish_word': 'angielski'}
        form_data3 = {}

        form1 = WordForm(data=form_data1)
        form2 = WordForm(data=form_data2)
        form3 = WordForm(data=form_data3)

        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertFalse(form3.is_valid())

    def test_empty_string(self):
        form_data1 = {'english_word': 'english', 'polish_word': ''}
        form_data2 = {'english_word': '',        'polish_word': 'angielski'}
        form_data3 = {'english_word': '',        'polish_word': ''}

        form1 = WordForm(data=form_data1)
        form2 = WordForm(data=form_data2)
        form3 = WordForm(data=form_data3)

        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertFalse(form3.is_valid())






