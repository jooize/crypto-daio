from django.db import models

# Create your models here.
from daio.models import Chain


class Exchange(models.Model):
    chain = models.ForeignKey(
        Chain,
        related_name='exchanges',
        related_query_name='exchange'
    )
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    api_base = models.URLField(max_length=500)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    get_usd_value = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'currencies'


class CurrencyValue(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    currency = models.ForeignKey(
        Currency,
        related_name='values',
        related_query_name='value'
    )
    usd_value = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return '{} {} = USD {}'.format(self.date_time, self.currency.code, self.usd_value)


class Pair(models.Model):
    name = models.CharField(max_length=255)
    exchange = models.ForeignKey(
        Exchange,
        related_name='pairs',
        related_query_name='pair'
    )
    base_currency = models.ForeignKey(
        Currency,
        related_name='base_currencies',
        related_query_name='base_currency',
        blank=True,
        null=True
    )
    quote_currency = models.ForeignKey(
        Currency,
        related_name='quote_currencies',
        related_query_name='quote_currency',
        blank=True,
        null=True
    )

    def __str__(self):
        return '{}/{}@{}'.format(
            self.quote_currency.code,
            self.base_currency.code,
            self.exchange
        )


class Balance(models.Model):
    pair = models.ForeignKey(
        Pair,
        related_name='balances',
        related_query_name='balance'
    )
    date_time = models.DateTimeField(auto_now=True)
    base_amount = models.DecimalField(
        max_digits=16,
        decimal_places=4,
        blank=True,
        null=True
    )
    quote_amount = models.DecimalField(
        max_digits=16,
        decimal_places=4,
        blank=True,
        null=True
    )

    def __str__(self):
        return '{} {}/{} {}'.format(
            self.pair.quote_currency.code,
            self.quote_amount,
            self.pair.base_currency.code,
            self.base_amount
        )


class Trade(models.Model):
    order_id = models.CharField(max_length=255)
    pair = models.ForeignKey(
        Pair,
        related_name='orders',
        related_query_name='order'
    )
    date_time = models.DateTimeField(blank=True, null=True)
    order_type = models.CharField(
        max_length=255,
        choices=[
            ('BUY', 'Buy'),
            ('SELL', 'Sell')
        ],
        blank=True,
        null=True
    )
    amount = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True)
    rate = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True)
    total = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True)
    fee = models.DecimalField(max_digits=26, decimal_places=10, blank=True, null=True)

    def __str__(self):
        return '{}@{}'.format(self.order_id, self.pair)

    class Meta:
        unique_together = ('order_id', 'pair')
        ordering = ('-date_time',)

