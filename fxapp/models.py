from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.utils import timezone
import uuid
import random
from django.core.validators import MinValueValidator
# import shortuuid
from django.conf import settings
# Creating models for the treasury fxapp


User = settings.AUTH_USER_MODEL


class Segment(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Segment'

class Customer(models.Model):
    cif = models.CharField(max_length=20,unique=True, blank=False)
    name = models.CharField(max_length=200,unique=True, blank=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Customer'


class Dealer(models.Model):
    full_name = models.CharField(max_length=100)
    profile = models.CharField(max_length=100, unique=True, default='profile')
    user = models.OneToOneField(User, unique=True, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile
    
    class Meta:
        verbose_name = 'Trader'

class Ccy(models.Model):
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.code

class SystemDailyRates(models.Model):
    date            = models.DateTimeField(default=timezone.now)
    ccy             = models.ForeignKey(Ccy, on_delete=models.CASCADE, blank=False)
    exchange_rate   = models.DecimalField(
        max_digits=10, decimal_places=4, default=1.00
    )
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)

    @property
    def ccy_code(self): 
        return self.ccy.code 

    class Meta:
        verbose_name_plural = 'Reevaluation Rates'
        ordering = ['-last_updated']
        # constraints = [
        #     models.UniqueConstraint(fields=['date', 'ccy'], name='unique_rate_per_currency_per_date')
        # ]

    def __str__(self):
        return f"{self.ccy.code} - {self.date}: {self.exchange_rate}"


class Product(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(default='Product description')

    def __str__(self):
        return self.name
    
class ExcelModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Trade(models.Model):


    BUYSELL = [
    ('buy', 'BUY'),
    ('sell', 'SELL'),
    ]

    STATUS = [
        ('verified', 'VERIFIED'),
        ('cancelled', 'CANCELLED'),
        ('matured', 'MATURED'),
        ('amend', 'AMEND'),
    ]

    trade_id            = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4)
    tx_date             = models.DateField(auto_now=True)
    val_date            = models.DateTimeField( blank=False, null=False, auto_now=False)
    ccy1                = models.ForeignKey(Ccy, on_delete=models.CASCADE, related_name="currency1",blank=False,null=False)
    ccy2                = models.ForeignKey(Ccy, on_delete=models.CASCADE, related_name='currency2',blank=False,null=False)
    # ccyPair             = models.CharField(max_length=2, default=1)
    buy_sell            = models.CharField(choices=BUYSELL, null=False, blank=False, max_length=100)
    amount1             = models.FloatField()
    amount2             = models.FloatField()
    deal_rate           = models.DecimalField(decimal_places=4,max_digits=10, default=1)
    fees_rate           = models.DecimalField(decimal_places=4, max_digits=10,default=1)
    system_rate         = models.DecimalField(decimal_places=4,max_digits=10,default=1)
    ccy1_rate           = models.DecimalField(decimal_places=4,max_digits=10,default=1)
    ccy2_rate           = models.DecimalField(decimal_places=4,max_digits=10,default=1)
    # deal_pnl          = models.DecimalField(decimal_places=4, max_digits=10)
    tx_comments         = models.CharField(max_length=200, blank=True)
    customer            = models.ForeignKey(Customer, on_delete=models.CASCADE,blank=False,null=False)
    product             = models.ForeignKey(Product, on_delete=models.CASCADE,blank=False,null=False)
    trader              = models.ForeignKey(Dealer, on_delete=models.CASCADE, blank=False,null=False)
    status              = models.CharField(choices=STATUS, null=False, blank=False, max_length=100,default='verified')
    # slug                = slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    date_created        = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    last_updated        = models.DateTimeField(blank=True, null=True, auto_now=True)
 
    @staticmethod
    def generate_unique_trade_id():
    # Use a random 4-digit number combined with a 3-digit counter
        # stamp = int(timezone.now(timezone(timedelta(hours=3))).strftime('%y-%m-%d'))
        counter = int(timezone.now(timezone(timedelta(hours=3)))) 
        random_part = random.randint(1, 99999)
        # f'{random_part:04d}{counter:03d}'
        return f'{random_part}{counter:05d}'
    
    @property
    def equivalent_lcy(self):
        return Decimal(self.amount1) * self.ccy1_rate
    
    @staticmethod
    def calculate_pnl(trade_instance):
        amount1 = trade_instance.amount1 if trade_instance.buy_sell == 'buy' else -trade_instance.amount1
        pnl = -Decimal(amount1) * (trade_instance.deal_rate - trade_instance.system_rate) * trade_instance.ccy2_rate
        return pnl
    
    @property
    def deal_pnl(self):
        return self.calculate_pnl(self)

    def __str__(self):
        return str(self.trade_id)[0:8]

    def __unicode__(self):
        return self.trade_id
    
    class Meta:
        verbose_name = 'Trade'

class Position(models.Model):
    date                = models.DateField( blank=False, null=False, auto_now=False)
    ccy                 = models.ForeignKey(Ccy, on_delete=models.CASCADE,blank=False,null=False)
    intraday_pos        = models.FloatField()


    # _calculated_net_open_pos = None  # Internal property to cache the calculated value

    def __str__(self):
        return f"{self.ccy.code} - {self.intraday_pos}"
    
    def get_open_pos(self):
        """
        Retrieves the most recent `net_open_pos` from before the current Position's date.
        """
        prev_pos = Position.objects.filter(
            date__lt=self.date,
            ccy=self.ccy
        ).order_by('-date').first()
        return prev_pos.intraday_pos if prev_pos else 0

    @property
    def open_pos(self):
        """
        Property that calculates the aggregate net_open_pos for the current Position instance.
        """
        return self.get_open_pos()
    
    @property
    def close_pos(self):
        """
        Property that calculates the aggregate net_open_pos for the current Position instance.
        """
        return float(self.open_pos) + float(self.intraday_pos)
    