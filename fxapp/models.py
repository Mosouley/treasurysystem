from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.utils import timezone
import uuid
import random

# import shortuuid
from django.conf import settings
from django.urls import reverse
from treasurysystem.utils import random_string_generator
from django.utils.text import slugify
# Creating models for the treasury fxapp


User = settings.AUTH_USER_MODEL


class Segment(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Segment'

class Customer(models.Model):
    cif = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, unique=True, null=True, blank=True, on_delete=models.CASCADE)
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
    desc = models.CharField(max_length=100)
    name = models.CharField(max_length=200, unique=True)
    user = models.OneToOneField(User, unique=True, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Trader'

class Ccy(models.Model):
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Ccy'
        verbose_name_plural = "Ccy"

    def __str__(self):
        return self.code

class SystemDailyRates(models.Model):
    date            = models.DateTimeField(auto_now=True, blank=False)
    ccy             = models.ForeignKey(Ccy, on_delete=models.CASCADE, blank=False)
    rateLcy         = models.FloatField(default=1.00)
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)

    @property
    def ccy_code(self): 
        return self.ccy.code 

    class Meta:
        verbose_name_plural = 'SystemRates'

    def __str__(self):
        return self.ccy.code 


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

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

    def generate_unique_trade_id():
    # Use a random 4-digit number combined with a 3-digit counter
        # stamp = int(timezone.now(timezone(timedelta(hours=3))).strftime('%y-%m-%d'))
        counter = int(timezone.now(timezone(timedelta(hours=3)))) 
        random_part = random.randint(1, 99999)
        # f'{random_part:04d}{counter:03d}'
        print(f'{random_part}{counter:05d}')
        return f'{random_part}{counter:05d}'
    
    trade_id            = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4)
    tx_date             = models.DateTimeField(auto_now=True)
    val_date            = models.DateTimeField( blank=False, null=False, auto_now=False)
    ccy1                = models.ForeignKey(Ccy, on_delete=models.CASCADE, related_name="currency1",blank=False,null=False)
    ccy2                = models.ForeignKey(Ccy, on_delete=models.CASCADE, related_name='currency2',blank=False,null=False)
    # ccyPair             = models.CharField(max_length=2, default=1)
    buy_sell            = models.CharField(choices=BUYSELL, null=False, blank=False, max_length=100)
    amount1             = models.FloatField()
    amount2             = models.FloatField()
    deal_rate           = models.DecimalField(decimal_places=4,max_digits=10)
    fees_rate           = models.DecimalField(decimal_places=4, max_digits=10)
    system_rate         = models.DecimalField(decimal_places=4,max_digits=10)
    ccy1_rate           = models.DecimalField(decimal_places=4,max_digits=10)
    ccy2_rate           = models.DecimalField(decimal_places=4,max_digits=10)
    # deal_pnl          = models.DecimalField(decimal_places=4, max_digits=10)
    tx_comments         = models.CharField(max_length=200, blank=True)
    customer            = models.ForeignKey(Customer, on_delete=models.CASCADE,blank=False,null=False)
    product             = models.ForeignKey(Product, on_delete=models.CASCADE,blank=False,null=False)
    trader              = models.ForeignKey(Dealer, on_delete=models.CASCADE, blank=False,null=False)
    status              = models.CharField(choices=STATUS, null=False, blank=False, max_length=100,default='verified')
    # slug                = slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    date_created        = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    last_updated        = models.DateTimeField(blank=True, null=True, auto_now=True)
 

    
    @property
    def equivalent_lcy(self):
        return Decimal(self.amount1) * self.ccy1_rate
    
    @property
    def deal_pnl(self):
        amount1 = Decimal(self.amount1)
        deal_rate = Decimal(self.deal_rate)
        system_rate = Decimal(self.system_rate)
        ccy2_rate = Decimal(self.ccy2_rate)
     #     return -self.amount1 * (self.deal_rate - self.system_rate) * obj.amount2
        return -(amount1 * (deal_rate - system_rate) * ccy2_rate)

    def __str__(self):
        return str(self.trade_id)

    def __unicode__(self):
        return self.trade_id
    
    class Meta:
        verbose_name = 'Trade'

    # def save(self, *args, **kwargs):
    #     # Ensure a unique trade_id is generated
    #     # Generate the slug when saving the model
    #     if not self.slug:
    #         base_slug = slugify(self.trade_id)
    #         unique_slug = base_slug
    #         counter = 1
    #         while Trade.objects.filter(slug=unique_slug).exists():
    #             unique_slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = unique_slug
    #     super().save(*args, **kwargs)

    # def __init__(self, *args, **kwargs):
    #     """
    #     Override the __init__ method to set the choices for the ccy_pair field when initializing the model.
    #     """
    #     super(Trade, self).__init__(*args, **kwargs)
    #     self._meta.get_field('trade_id').default = uuid4()
    #     self._meta.get_field('ccy_pair').choices = self.get_ccy_pair_choices()
    

    # def update_total(self):
    #     cart_total     = self.cart.total
    #     shipping_total = self.shipping_total
    #     new_total      =  math.fsum([cart_total , shipping_total])
    #     formatted_total = format(new_total, '.2f')
    #     self.total     = formatted_total
    #     self.save()
    #     return new_total


    # def get_absolute_url(self):
    #     return reverse('trade-detail', kwargs={'slug': self.slug})


    # def save(self, *args, **kwargs):
    #     if self.date_created is None:
    #         self.date_created = timezone.localtime(timezone.now())
    #     if self.trade_id is None:
    #         new_ref = random_string_generator(10)
    #         self.trade_id = new_ref.join(str(uuid4()).split('-')[4])
    #         print(self.trade_id)
    #         self.slug = slugify('{}{}'.format( self.trade_id))
    #     if not self.trade_id:
    #         self.trade_id = str(uuid4())[:8]

    #     self.slug = slugify('{}'.format( self.trade_id))
    #     self.last_updated = timezone.localtime(timezone.now())
    #     # self._meta.get_field('ccy_pair').choices = self.get_ccy_pair_choices()
    #     super(Trade, self).save(*args, **kwargs)