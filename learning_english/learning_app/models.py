from django.db import models


class Word(models.Model):
    english_word = models.CharField(max_length=100)
    polish_word = models.CharField(max_length=100)
    level_of_knowledge_english = models.IntegerField(default=1)
    level_of_knowledge_polish = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.english_word} {self.level_of_knowledge_english} -" \
               f" {self.level_of_knowledge_polish} {self.polish_word}"


class Answer(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word} {self.text} {self.language} {self.data} {self.is_correct}"

    @property
    def is_correct(self):
        if self.language == 'english':
            if self.text == self.word.english_word:
                return True
            else:
                return False
        elif self.language == 'polish':
            if self.text == self.word.polish_word:
                return True
            else:
                return False
        else:
            raise ValueError('Wrong language!')
