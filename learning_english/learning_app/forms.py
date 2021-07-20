from django import forms


class WordForm(forms.Form):
    english_word = forms.CharField(max_length=50)
    polish_word = forms.CharField(max_length=50)