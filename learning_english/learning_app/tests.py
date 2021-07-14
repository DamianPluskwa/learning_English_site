from django.test import TestCase
from django.utils import timezone

from .models import Word, Answer


class WordModelTests(TestCase):

    def test_create_instance_of_word(self):
        word = Word(english_word='english', polish_word='angielski')
        self.assertIsInstance(word, Word)

    def test_str_method(self):
        word = Word(english_word='english', polish_word='angielski')
        self.assertEqual(str(word), 'english 1 - 1 angielski')

    def test_every_attribute(self):
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
