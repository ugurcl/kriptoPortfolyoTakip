from django.db import models
from django.contrib.auth.models import User



class userPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='') 
    portfolio_name = models.CharField(
        verbose_name='Portfolyo Adı',
        max_length=300,
    )


    def __str__(self):
        return self.portfolio_name


class Portfolio(models.Model):
    ASSET_TYPES = [
        ('gold', 'Altın'),
        ('crypto', 'Kripto Para'),
        ('currency', 'Döviz'),
    ]
    portfolio = models.ForeignKey(userPortfolio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    asset_name = models.CharField(max_length=100) 
    amount = models.FloatField()
    buy_price = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True) 

   
    def __str__(self):
        return f"{self.asset_name} - {self.amount} {self.asset_type}"

    def get_profit_or_loss(self, current_price):
        try:
            buy_price_decimal = float(self.buy_price)
            amount_decimal = float(self.amount)
            current_price_decimal = float(current_price)

            profit_or_loss = (current_price_decimal - buy_price_decimal) * amount_decimal

            if buy_price_decimal == 0:
                percentage = 0
            else:
                percentage = ((current_price_decimal / buy_price_decimal) * 100) - 100

            return {
                "amount": round(profit_or_loss, 2),
                "percentage": round(percentage, 2)
            }
        except:
            return {
            "amount": 0,
            "percentage": 0
        }