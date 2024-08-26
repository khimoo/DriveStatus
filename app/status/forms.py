from django import forms


class ReservationForm(forms.Form):
    name = forms.CharField(
            label='ユーザー名',
            max_length=100,
            widget=forms.TextInput(attrs={'class': 'form-control'})
            )
    password = forms.CharField(max_length=100)
    start_date = forms.DateTimeField(
            label='開始日時',
            widget=forms.DateTimeInput(attrs={'class': 'form-control'})
            )
    usage_time = forms.IntegerField()
