# Generated by Django 3.0.4 on 2020-03-07 17:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PagarmeFormConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('max_installments', models.IntegerField(default=12, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('default_installment', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('free_installment', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('interest_rate', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('payments_methods', models.CharField(choices=[('boleto', 'Somente Boleto'), ('credit_card', 'Somente Cartão de Crédito'), ('credit_card,boleto', 'Cartão de Crédito ou Boleto')], default='credit_card,boleto', max_length=18)),
            ],
            options={
                'verbose_name': 'Configuração de Pagamento',
                'verbose_name_plural': 'Configurações de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='PagarmeItemConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128)),
                ('price', models.PositiveIntegerField(verbose_name='Preço em Centavos')),
                ('tangible', models.BooleanField(verbose_name='Produto físico?')),
                ('default_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_items', to='django_pagarme.PagarmeFormConfig')),
            ],
            options={
                'verbose_name': 'Configuração de Item de Pagamento',
                'verbose_name_plural': 'Configurações Itens de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='PagarmePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('boleto', 'Boleto'), ('credit_card', 'Cartão de Crédito')], max_length=11)),
                ('transaction_id', models.CharField(db_index=True, max_length=50, unique=True)),
                ('amount', models.PositiveIntegerField(verbose_name='Preço pago em Centavos')),
                ('card_id', models.CharField(max_length=64, null=True)),
                ('card_last_digits', models.CharField(max_length=4, null=True)),
                ('boleto_url', models.TextField(null=True)),
                ('boleto_barcode', models.TextField(null=True)),
                ('installments', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Parcelas')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='PagarmePaymentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_pagarme.PagarmeItemConfig')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_pagarme.PagarmePayment')),
            ],
            options={
                'verbose_name': 'Item de Pagamento',
                'verbose_name_plural': 'Items de Pagamento',
                'unique_together': {('payment', 'item')},
            },
        ),
        migrations.AddField(
            model_name='pagarmepayment',
            name='items',
            field=models.ManyToManyField(related_name='payments', through='django_pagarme.PagarmePaymentItem', to='django_pagarme.PagarmeItemConfig'),
        ),
        migrations.AddField(
            model_name='pagarmepayment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PagarmeNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('status', models.CharField(choices=[('processing', 'Processando'), ('authorized', 'Autorizado'), ('paid', 'Pago'), ('refunded', 'Estornado'), ('pending_refund', 'Estornando'), ('waiting_payment', 'Aguardando Pgto'), ('refused', 'Recusado')], max_length=30)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='django_pagarme.PagarmePayment')),
            ],
            options={
                'verbose_name': 'Notificação de Pagamento',
                'verbose_name_plural': 'Notificações de Pagamento',
                'ordering': ('-creation',),
            },
        ),
        migrations.AddIndex(
            model_name='pagarmepayment',
            index=models.Index(fields=['user', '-id'], name='pargarme_payments_user'),
        ),
        migrations.AddIndex(
            model_name='pagarmenotification',
            index=models.Index(fields=['-creation', 'payment'], name='notification_payment_creation'),
        ),
    ]