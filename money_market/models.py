from decimal import Decimal
from django.db import models
from django.utils import timezone
import random
import string

from fxapp.models import Ccy, Dealer
from treasurysystem.utils import calculate_interest
# Create your models here.

# Create your models here.
class LimitType(models.Model):
    CATEGORY = [
            ('balance-sheet', 'BALANCE SHEET'),
            ('off-balance-sheet', 'OFF BALANCE SHEET'),
            ]
    short_name          = models.CharField(max_length=25, unique=True)
    full_name         = models.TextField(default='Full name of the limit')
    category            = models.CharField(choices=CATEGORY, null=False, blank=False, max_length=25)
    def __str__(self):
        return self.short_name
    
class Counterparty(models.Model):
    CATEGORY = [
            ('non-group', 'Non-group'),
            ('group', 'Group'),
            ]
    name                = models.CharField(max_length=25, unique=True, blank=True, null=True) #Important to not have null=False 
    short_name          = models.CharField(max_length=25, unique=True)
    description         = models.TextField(default='Full name counterparty')
    category            = models.CharField(choices=CATEGORY, null=False, blank=False, max_length=25)
    def __str__(self):
        return self.short_name
    
class Limits(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,blank=False,null=False)
    limit_type      = models.ForeignKey(LimitType, on_delete=models.CASCADE, null=False, blank=False)
    limit_amount    = models.FloatField()
    limit_approval_date = models.DateField(blank=False, null=False,)
    limit_maturity      = models.DateField(blank=False, null=False,)
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.counterparty_short_name
    
class Exposures(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,blank=False,null=False)
    limit_type      = models.ForeignKey(LimitType, on_delete=models.CASCADE, null=False, blank=False)
    exposure_amount    = models.FloatField()
    
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)
    def __str__(self):
        return self.counterparty_short_name
    
class LimitException(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,blank=False,null=False)
    limit_type      = models.ForeignKey(LimitType, on_delete=models.CASCADE, null=False, blank=False)
    exception_amount    = models.FloatField()
    exception_date   = models.DateField(default=timezone.now)
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)
    def __str__(self):
        return self.counterparty_short_name
    

class Approvals(models.Model):
    CATEGORY = [
            ('annual', 'ANNUAL REVIEW'),
            ('interim', 'INTERIM REVIEW'),
            ('initial', 'INITIAL REVIEW'),
            ('exception', 'EXCEPTION APPROVAL'),
            ]
    counterparty        = models.ForeignKey(Counterparty, on_delete=models.CASCADE,blank=False,null=False)
    approval_type       = models.CharField(CATEGORY,  null=False, blank=False, max_length=25)
    document            = models.FileField(
        upload_to='approval_documents/',  # Folder where uploaded files will be stored
        null=False,
        blank=False
    )
    exception_amount    = models.FloatField()
    approval_date       = models.DateField(default=timezone.now)
    last_updated        = models.DateTimeField(blank=True, null=True, auto_now=True)
    def __str__(self):
        return f"Approval for {self.counterparty} - {self.CATEGORY()}"
    
class Product(models.Model):
    PRODUCT_CHOICES = [
        ('PLX', 'Placement'),
        ('SPOT', 'FX SPOT'),
        ('FWD', 'FX FWD'),
        ('SWAP', 'FX SWAP'),
        ('GUARANTEE', 'Guarantee'),
        ('LC', 'Letter of Credit'),
        ('Discount', 'Discount of Instrument'),
    ]
    DAYS_CONVENTION = [
        ('ACT/360', 'Actual/360'),
        ('ACT/365', 'Actual/365'),
        ('30/360', '30/360'),
        ('ACT/ACT', 'Actual/Actual'),
    ]

    code = models.CharField(choices=PRODUCT_CHOICES, max_length=10, unique=True)
    limit_type = models.ForeignKey(LimitType, on_delete=models.CASCADE, null=False, blank=False)
    days_convention = models.CharField(choices=DAYS_CONVENTION, max_length=10)

    def __str__(self):
        return self.code


def generate_unique_trade_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Deal(models.Model):
    PAYRECV = [
        ('PAY', 'Pay'),
        ('RECV', 'Receive'),
    ]
    STATUS = [
        ('VERIFIED', 'Verified'),
        ('PENDING', 'Pending'),
        ('REJECTED', 'Rejected'),
    ]

    trade_id = models.CharField(max_length=6, unique=True, default=generate_unique_trade_id)
    pay_recv = models.CharField(choices=PAYRECV, max_length=100)
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    maturity_date = models.DateField()
    tx_comments = models.CharField(max_length=200, blank=True)
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    trader = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=100, default='verified')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.trade_id

    def calculate_interest(self):
        return calculate_interest(
            self.principal_amount,
            self.interest_rate,
            self.start_date,
            self.maturity_date,
            self.product.days_convention
        )
    class Meta:
        verbose_name = 'Deal'
        indexes = [
            models.Index(fields=['trade_id']),
            models.Index(fields=['counterparty']),
        ]
