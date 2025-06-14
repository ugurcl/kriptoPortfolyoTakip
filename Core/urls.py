from django.urls import path
from Core.views import (
    Dashboard,
    Index,
    LoginView,
    CryptoMarketsView,
    GoldsPage,
    ExchangeRatesView,
    PortfolioView,
    AddNewPortfolio,
    SignUpView,
    PortfolioDeleteView,
    LogoutView
)


urlpatterns = [

    path('anasayfa/', Dashboard.as_view(), name='dashboard'),
    path('', Index.as_view(), name='index'),
    path('giris-yap/', LoginView.as_view(), name='login'),
    path('kripto-paralar/', CryptoMarketsView.as_view(), name='cryptomarkets' ),
    path('altin/', GoldsPage.as_view(), name='golds' ),
    path('dovizler/', ExchangeRatesView.as_view(), name='exchangeRates' ),
    path('portfolyo/', PortfolioView.as_view(), name='portfolio' ),
    path("portfolyo-ekle/", AddNewPortfolio.as_view(), name="add_portfolio"),
    path('kayit-ol/', SignUpView.as_view(), name='signup'),
    path('portfolio/delete/<int:pk>/', PortfolioDeleteView.as_view(), name='portfolio-delete'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
