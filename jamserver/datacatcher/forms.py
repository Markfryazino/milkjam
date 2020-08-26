from django import forms


class TimeoutForm(forms.Form):
    timeout = forms.IntegerField()
