from django import forms
from .models import userPortfolio
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Kullanıcı adınızı girin',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Şifrenizi girin',
        })
    )


class PortfolioCreateForm(forms.Form):
    name = forms.CharField(
        label="Portföy Adı",
        max_length=300,
        widget=forms.TextInput(attrs={
            'placeholder': 'Portföyo Adı',
            'class': 'form-control'
        })
    )

    
class AssetForm(forms.Form):

    CATEGORY_CHOICES = [
        ('', 'Seçiniz'),
        ('gold', 'Altın'),
        ('crypto', 'Kripto Para'),
        ('currency', 'Döviz'),
    ]
    portfolio = forms.ModelChoiceField(
        queryset=userPortfolio.objects.none(), 
        label='Portföy Seç',
        widget=forms.Select(attrs={'id': 'portfolio'})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label='Varlık Türü Seç',
        widget=forms.Select(attrs={'id': 'category'})
    )

    asset = forms.ChoiceField(
        choices=[('', 'Önce tür seç')],
        label='Varlık Seç',
        widget=forms.Select(attrs={'id': 'asset'})
    )

    price = forms.CharField(
        label='Alış Fiyatı (otomatik)',
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'id': 'price'})
    )

    amount = forms.DecimalField(
        label='Adet / Miktar',
        min_value=0,
        decimal_places=4,
        required=True,
        widget=forms.NumberInput(attrs={'step': '0.0001', 'id': 'amount'})
    )


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['portfolio'].queryset = userPortfolio.objects.filter(user=user)

        if 'data' in kwargs:
            data = kwargs['data']
        elif args:
            data = args[0]
        else:
            data = {}

        category = data.get('category')
        asset_choices = [('', 'Seçiniz')]

        if category == 'crypto':
            from Utils.crypto import getTopPairs
            cryptos = getTopPairs(10)
            asset_choices += [(coin['symbol'], coin['symbol']) for coin in cryptos]
        elif category == 'gold':
            from Utils.exchange_rates import gold_prices
            golds = gold_prices()
            asset_choices += [(gold['title'], gold['title']) for gold in golds]
        elif category == 'currency':
            from Utils.exchange_rates import get_all_exchange_rates
            currencies = get_all_exchange_rates()
            asset_choices += [(k, v['name']) for k, v in currencies.items()]

        self.fields['asset'].choices = asset_choices





from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Kullanıcı adınızı girin',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Parolanızı girin',
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Parolanızı tekrar girin',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Kullanıcı Adı',
            'password1': 'Parola',
            'password2': 'Parola (Tekrar)',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten mevcut.")
        return username
