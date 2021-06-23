from django import forms


class AnswerForm(forms.Form):
    text = forms.CharField(max_length=100)
