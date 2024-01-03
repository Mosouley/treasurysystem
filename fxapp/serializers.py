from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Customer, Ccy, Segment, Product,Dealer,SystemDailyRates,Trade
from django.db import transaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('__all__')

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ['name', 'desc']


class CcySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ccy
        fields = ['code']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')


class SystemDailyRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemDailyRates
        fields = ('date', 'last_updated', 'rateLcy', 'ccy', 'ccy_code')
        # print(fields)

    # def get_ccy_entity(self):
    #     ccy = SystemDailyRates.objects.get(pk=self.id)
    #     print(ccy)
    #     return ccy

class TradeSerializer(serializers.ModelSerializer):
    equivalent_lcy = serializers.SerializerMethodField()
    gross_pnl = serializers.SerializerMethodField()
    net_pnl = serializers.SerializerMethodField()

    class Meta:
        model = Trade
        # fields = '__all__'
        fields = ['trade_id', 'tx_date', 'val_date', 'customer', 'product', 'trader', 'ccy1', 'ccy2', 'ccy_pair', 'buy_sell', 'amount1', 'amount2', 'deal_rate', 'fees_rate', 'system_rate', 'cover_rate', 'tx_comments',  'active', 'slug', 'date_created', 'last_updated', 'equivalent_lcy', 'gross_pnl', 'net_pnl']



    def get_equivalent_lcy(self, obj):
        return Decimal(obj.amount1) * obj.deal_rate

    def get_gross_pnl(self, obj):
        return 89000

    def get_net_pnl(self, obj):
        return 0

        # add transaction.atomic so that if error happened, it will rollback
    # @transaction.atomic
    # def create(self, validated_data):
    #     trade = Trade.objects.create(**validated_data)
    #     if "products" in self.initial_data:
    #         products = self.initial_data.get("products")
    #         for product in products:
    #             quantity = product.get("quantity")
    #             product = Product.objects.get(pk=id)
    #             Detail(order=order, product=product, quantity=quantity).save()
    #     order.save()
    #     return order