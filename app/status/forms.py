from django import forms


class ReservationForm(forms.Form):
    name = forms.CharField(
        label="ユーザー名",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(max_length=100)
    start_date = forms.DateTimeField(
        label="開始日時",
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "id": "start_date",
                "placeholder": "YYYY-MM-DD HH:MM",
            },
            format="%Y-%m-%d %H:%M",
        ),
    )
    end_date = forms.DateTimeField(
        label="終了日時",
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "id": "end_date",
                "placeholder": "YYYY-MM-DD HH:MM",
            },
            format="%Y-%m-%d %H:%M",
        ),
    )


class GasolineForm(forms.Form):
    name = forms.CharField(
        label="給油した人",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    price = forms.IntegerField(
        label="金額",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    # blank=True
    comment = forms.CharField(
        label="備考",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
