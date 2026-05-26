from django import forms


class ConsultaCadeadoForm(forms.Form):
    id_cadeado = forms.CharField(
        label='ID do cadeado',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o ID do cadeado',
            'class': 'form-control'
        })
    )