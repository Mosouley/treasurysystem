from django.db import models
from django.utils import timezone
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
        return self.name
    
class Counterparty(models.Model):
    CATEGORY = [
            ('non-group', 'NON-GROUP'),
            ('group', 'GROUP'),
            ]
    name                = models.CharField(max_length=25, unique=True, blank=False, null=False)
    short_name          = models.CharField(max_length=25, unique=True)
    description         = models.TextField(default='Full name counterparty')
    category            = models.CharField(choices=CATEGORY, null=False, blank=False, max_length=25)
    def __str__(self):
        return self.name
    
class Limits(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,blank=False,null=False)
    limit_type      = models.ForeignKey(LimitType, on_delete=models.CASCADE, null=False, blank=False)
    limit_amount    = models.FloatField()
    limit_approval_date = models.DateField(blank=False, null=False,)
    limit_maturity      = models.DateField(blank=False, null=False,)
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.counterparty__shortname
    
class Exposures(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,blank=False,null=False)
    limit_type      = models.ForeignKey(LimitType, on_delete=models.CASCADE, null=False, blank=False)
    exposure_amount    = models.FloatField()
    
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)
    def __str__(self):
        return self.counterparty__shortname
    
class LimitException(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,blank=False,null=False)
    limit_type      = models.ForeignKey(LimitType, on_delete=models.CASCADE, null=False, blank=False)
    exception_amount    = models.FloatField()
    exception_date   = models.DateField(default=timezone.now)
    last_updated    = models.DateTimeField(blank=True, null=True, auto_now=True)
    def __str__(self):
        return self.counterparty__shortname
    

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