from django import forms


class WordForm(forms.Form):
    english_word = forms.CharField(label='Słowo angielskie:', max_length=50)
    polish_word = forms.CharField(label='Słowo polskie:', max_length=50)