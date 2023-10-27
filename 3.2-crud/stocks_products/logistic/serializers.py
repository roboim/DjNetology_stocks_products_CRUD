from django.core.validators import MinValueValidator
from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    """Вывод информации по продукту"""
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']  #'__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    """Вывод информации для позиции продукту на складе"""
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True
    )
    quantity = serializers.IntegerField(min_value=1, default=1)
    price = serializers.DecimalField(max_digits=18, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        model = Stock
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    """Вывод информации по складам"""
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # заполняем связанную таблицу: StockProduct
        for pos_string in positions:
            StockProduct.objects.create(quantity=pos_string['quantity'], price=pos_string['price'],
                                        product_id=pos_string['product'].id, stock_id=stock.id)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # обновляем связанную таблицу: StockProduct
        for pos_string in positions:
            counter = StockProduct.objects.filter(stock_id=stock.id, product_id=pos_string['product'].id).count()
            if counter != 0:
                StockProduct.objects.filter(stock_id=stock.id, product_id=pos_string['product'].id).update(
                    quantity=pos_string['quantity'], price=pos_string['price'],
                    product_id=pos_string['product'].id, stock_id=stock.id)
            else:
                StockProduct.objects.create(quantity=pos_string['quantity'], price=pos_string['price'],
                                            product_id=pos_string['product'].id, stock_id=stock.id)

        return stock
