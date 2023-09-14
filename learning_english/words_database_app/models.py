from django.db import models


class PolishWord(models.Model):
    word = models.CharField(max_length=100)


class EnglishWord(models.Model):
    word = models.CharField(max_length=100)


class WordTranslation(models.Model):
    polish_word = models.ForeignKey(PolishWord, on_delete=models.CASCADE)
    english_word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)
