from django import forms


class TimeLineForm(forms.Form):
    title = forms.CharField(max_length=30, min_length=6)
    content = forms.CharField(widget=forms.Textarea)
