import decimal
from uuid import UUID
from rest_framework import serializers
from .models import Limits,LimitType, Counterparty, Exposures, LimitException, Approvals, Deal, Product
from rest_framework.fields import Field
from decimal import Decimal



class UUIDField(Field):
    def to_representation(self, value):
        if value is None:
            return None
        if isinstance(value, UUID):
            return str(value)
        return value
    
class CounterpartySerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='user.username', read_only=True)  # Retrieve username instead of user id
    # segment = serializers.CharField(source='segment.name', read_only=True)  # Retrieve segment name instead of segment id
    class Meta:
        model = Counterparty
        fields = ('__all__')
        extra_kwargs = {
            'short_name': {'validators': []}, 
            'name': {'validators': []},
        }

class LimitsSerializer(serializers.ModelSerializer):
    # counterparty = serializers.CharField(source='counterparty.short_name', read_only=True)
    counterparty = serializers.CharField(source='counterparty.short_name')
    limit_type = serializers.CharField(source='limit_type.short_name')
    class Meta:
        model = Limits
        fields = ('counterparty','limit_type', 'limit_amount','limit_approval_date','limit_maturity','last_updated', )


class ExposuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exposures
        fields = ('__all__')
        # fields = ['name', 'desc']

class LimitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitType
        fields = ('__all__')
        # fields = ['code']
        extra_kwargs = {
            'short_name': {
                'validators': [],
            }
        }

class LimitExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitException
        fields = ('__all__')
        # extra_kwargs = {
        #     'name': {
        #         'validators': [],
        #     }
        # }

class ApprovalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approvals
        fields = ('__all__')

class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ('__all__')


class ProductSerializer(serializers.ModelSerializer):
    product_choices = serializers.SerializerMethodField()
    days_convention_choices = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'code', 'limit_type', 'days_convention', 'product_choices', 'days_convention_choices']

    def get_product_choices(self, obj):
        return Product.PRODUCT_CHOICES

    def get_days_convention_choices(self, obj):
        return Product.DAYS_CONVENTION