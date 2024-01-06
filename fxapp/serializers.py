from decimal import Decimal
from rest_framework import serializers
from .models import Customer, Ccy, Segment, Product,Dealer,SystemDailyRates,Trade

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
    deal_pnl = serializers.ReadOnlyField()
    trade_id = serializers.ReadOnlyField()
    product = ProductSerializer()
    trader = DealerSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Trade
        fields = '__all__'       
        # fields = [ 'trade_id','tx_date', 'val_date', 'customer', 'product', 'trader', 'ccy1', 'ccy2', 'buy_sell', 'amount1', 'amount2', 'deal_rate', 'fees_rate', 'system_rate','equivalent_lcy', 'deal_pnl', 'tx_comments',  'active', 'slug', 'date_created', 'last_updated']

# serializer = TradeSerializer(data={
#     'tx_date': 'tx_date',
#     'val_date':'val_date',
#     'customer':'customer',
#     'product':'product', 
#     'trader':'trader', 
#     'ccy1':'ccy1', 
#     'ccy2':'ccy2',
#     'buy_sell':'buy_sell', 
#     'amount1':'amount1' ,
#     'amount2':'amount2',
#     'deal_rate':'deal_rate', 
#     'fees_rate':'fees_rate', 
#     'system_rate':'system_rate',
#     'tx_comments':'txt_comments', 
#     'active':'active', 
#     'slug':'slug',
#     'date_created':'date_created', 
#     'last_updated':'last_updated',
#     'equivalent_lcy':'equivalent_lcy', 
#     'deal_pnl':'deal_pnl'
# })
# if serializer.is_valid():
#     trade_instance = serializer.save()
# else:
#     print('printing your error message')
#     print(serializer.errors)

    def get_equivalent_lcy(self, obj):
        return Decimal(obj.amount1) * obj.deal_rate

    # def get_deal_pnl(self, obj):
    #     print(self)
    #     print(obj)
    #     return -self.amount1 * (self.deal_rate - self.system_rate) * obj.amount2

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