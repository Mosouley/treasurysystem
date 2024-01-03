from django.db import models
from django.utils import timezone
from uuid import uuid4
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
    trade_id            = models.UUIDField( default=uuid4())
    tx_date             = models.DateTimeField(auto_now=True)
    val_date            = models.DateTimeField( blank=False, null=False, auto_now=True)
    ccy1                = models.ForeignKey(Ccy, on_delete=models.CASCADE, related_name="currency1")
    ccy2                = models.ForeignKey(Ccy, on_delete=models.CASCADE, related_name='currency2')
    # ccyPair             = models.CharField(max_length=2, default=1)
    buy_sell            = models.CharField(choices=BUYSELL, null=False, blank=False, max_length=100)
    amount1             = models.FloatField()
    amount2             = models.FloatField()
    deal_rate           = models.DecimalField(decimal_places=4,max_digits=10)
    fees_rate           = models.DecimalField(decimal_places=4, max_digits=10)
    system_rate         = models.DecimalField(decimal_places=4,max_digits=10)
    deal_pnl          = models.DecimalField(decimal_places=4, max_digits=10)
    tx_comments         = models.CharField(max_length=200, blank=True)
    customer            = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    trader              = models.ForeignKey(Dealer, on_delete=models.CASCADE, blank=False,null=False)
    active              = models.BooleanField(default=True)
    slug                = models.SlugField(max_length=500, unique=True, default=slugify( trade_id))
    date_created        = models.DateTimeField(blank=True, null=True, auto_created=True)
    last_updated        = models.DateTimeField(blank=True, null=True, auto_now=True)
 
    
    @property
    def equivalent_lcy(self):
        return self.amount1 * self.deal_rate
    
    @property
    def gross_pnl(self):
        return 89000.00
    @property
    def net_pnl(self):
        return 0.00
    

    def __str__(self):
        return self.trade_id

    def __unicode__(self):
        return self.trade_id
    
    class Meta:
        verbose_name = 'Trade'

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


    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.trade_id is None:
            new_ref = random_string_generator(10)
            self.trade_id = new_ref.join(str(uuid4()).split('-')[4])
            print(self.trade_id)
            self.slug = slugify('{}{}'.format( self.trade_id))
        if not self.trade_id:
            self.trade_id = str(uuid4())[:8]

        self.slug = slugify('{}'.format( self.trade_id))
        self.last_updated = timezone.localtime(timezone.now())
        # self._meta.get_field('ccy_pair').choices = self.get_ccy_pair_choices()
        super(Trade, self).save(*args, **kwargs)