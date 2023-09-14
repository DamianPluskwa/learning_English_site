from django.test import TestCase
from .models import PolishWord, EnglishWord, WordTranslation


class PolishWordModelTests(TestCase):
    def test_create_instance_of_PolishWord(self):
        word = PolishWord(word='słowo')
        self.assertIsInstance(word, PolishWord)
        self.assertEqual(word.word, 'słowo')


class EnglishWordModelTests(TestCase):
    def test_create_instance_of_EnglishWord(self):
        word = EnglishWord(word='word')
        self.assertIsInstance(word, EnglishWord)
        self.assertEqual(word.word, 'word')


class WordTranslationModelTests(TestCase):
    def test_create_instance_of_WordTranslation(self):
        word_e = EnglishWord(word='word')
        word_p = PolishWord(word='słowo')
        translation = WordTranslation(polish_word=word_p, english_word=word_e)
        self.assertIsInstance(translation, WordTranslation)
        self.assertIsInstance(word_p, PolishWord)
        self.assertIsInstance(word_e, EnglishWord)
        self.assertEqual(translation.polish_word.word, 'słowo')
        self.assertEqual(translation.english_word.word, 'word')
