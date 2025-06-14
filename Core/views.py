from django.views import View
from django.shortcuts import render, redirect
from .forms import LoginForm, AssetForm, PortfolioCreateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from Utils.crypto import (
    getTopPairs,
    get_crypto_price,
)
from .utils import convert_price
from Utils.exchange_rates import gold_prices, get_all_exchange_rates, getOneExchangeRates, get_gold_price
from concurrent.futures import ThreadPoolExecutor
from .models import userPortfolio, Portfolio
from django.contrib import messages
from .forms import SignUpForm
from django.shortcuts import redirect, get_object_or_404
class LoginView(View):
    template_name = "pages/login.html"
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form':form
            }
        )
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request=request,
                username=username,
                password=password
            )

            if user is not None:
                login(request=request, user=user)
                return redirect('dashboard')
            else:
                form.add_error(None, "Kullanıcı adı veya şifre yanlış")
                return render(
                    request=request,
                    template_name=self.template_name,
                    context={
                        'form':form
                    }
                )
                

        else:
            return render(
                request=request,
                template_name=self.template_name,
                context={
                    'form':form
                }
            )
        
class Index(View):

    def get(self, request, *args, **kwargs):
        coin_list = getTopPairs(10)
        if not request.user.is_authenticated:
            return render(
                request=request,
                template_name='pages/index.html',
                context={
                    'coins':coin_list
                }
            )
        else :
            return redirect("dashboard")
        


class Dashboard(LoginRequiredMixin,View):
    login_url = '/giris-yap/'
    template_name = "pages/dashboard.html"
    def get(self, request, *args, **kwargs):
       
        portfolio = []
        selected_portfolio_id = request.GET.get('portfolio_id')
        user = request.user
        portfolios = Portfolio.objects.filter(user=user)

        if selected_portfolio_id:
            portfolios = portfolios.filter(portfolio__id=selected_portfolio_id)    

        for item in portfolios:
            if item.asset_type == 'crypto':
                current_price = get_crypto_price(symbol=item.asset_name)
            elif item.asset_type == 'currency':
                current_price = getOneExchangeRates(symbol=item.asset_name)
            elif item.asset_type == 'gold':
                current_price = get_gold_price(gold_name=item.asset_name)


            profit_or_loss = item.get_profit_or_loss(current_price)
            if isinstance(current_price, dict):
                current_price_value = current_price.get('price', 0)
            else:
                current_price_value = current_price
            
            portfolio.append({
                'date':item.date_added,
                'asset_name': item.asset_name,
                'asset_type': item.asset_type,
                'amount': item.amount,
                'id':item.id,
                'buy_price': str(item.buy_price),
                'current_price': str(current_price_value),
                'profit_or_loss': profit_or_loss,
                'portfolio_name':item.portfolio.portfolio_name,
                
                
            })
            
       
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'portfolio': portfolio,
                'select_portfolio':userPortfolio.objects.filter(user=request.user)
            }
        )


class PortfolioDeleteView(View):
    def post(self, request, pk):
        portfolio_item = get_object_or_404(Portfolio, pk=pk, user=request.user)

        portfolio_item.delete()
        
        return redirect('dashboard')
    

class CryptoMarketsView(LoginRequiredMixin, View):
    template_name = "pages/markets.html"
    def get(self, request, *args, **kwargs):
        search = request.GET.get("search")
        coin = None

        if search:
            coin = get_crypto_price(search.upper())
            return render(request, self.template_name, {'coin': coin})

        alldata = getTopPairs(10)

        return render(request, self.template_name, {
            'coins': alldata
        })

    

class GoldsPage(LoginRequiredMixin, View):
    template_name = 'pages/golds.html'
    def get(self, request, *args, **kwargs):
        golds_price = gold_prices()
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'gold':golds_price
            }
        )
    
class ExchangeRatesView(LoginRequiredMixin, View):
    template_name = 'pages/exchange_rates.html'
    def get(self, request, *args, **kwargs):
        exhange_rates = get_all_exchange_rates()
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'exchange':exhange_rates
            }
        )
    
class PortfolioView(LoginRequiredMixin, View):
    template_name = 'pages/portfolio.html'
    form = AssetForm
    def get(self, request, *args, **kwargs):
        form = self.form(user=request.user )
        with ThreadPoolExecutor() as executor:
            future_exchange = executor.submit(get_all_exchange_rates)
            future_golds = executor.submit(gold_prices)
            future_crypto = executor.submit(getTopPairs, 10)

            exchange_rates = future_exchange.result()
            golds = future_golds.result()
            cryptoMarketDataList = future_crypto.result()

        return render(
            request=request,
            template_name=self.template_name,
            context={
                'golds': golds,
                'crypto': cryptoMarketDataList,
                'exchange': exchange_rates,
                'form':form
            }
        )
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data
          
            Portfolio.objects.create(
                portfolio=cd['portfolio'],
                user=request.user,
                asset_type=cd['category'],
                asset_name=cd['asset'],
                amount=float(cd['amount']),
                buy_price= float(convert_price(cd['price']))
            )
 
            return redirect(request.path)
        else:
           
            return redirect(request.path)


class AddNewPortfolio(LoginRequiredMixin, View):
    template_name = 'pages/add_portfolio.html'
    form = PortfolioCreateForm
    def get(self, request, *args, **kwargs):
        form = self.form
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form':form
            }
        )
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            portfolio_name = form.cleaned_data.get('name')
            userPortfolio.objects.create(portfolio_name=portfolio_name, user=request.user)
            return redirect(request.path)
        else:
            return redirect(request.path)
        


class SignUpView(View):
    template_name = 'pages/register.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Kayıt başarılı! Giriş yapabilirsiniz.")
            return redirect('login') 
        else:
            messages.error(request, "Lütfen formu doğru doldurun.")
            return render(request, self.template_name, {'form': form})
        

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  