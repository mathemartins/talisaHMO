# Generated by Django 3.1.2 on 2021-06-27 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billing', '0001_initial'),
        ('insuranceplans', '0001_initial'),
        ('carts', '0001_initial'),
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=120)),
                ('shipping_address_final', models.TextField(blank=True, null=True)),
                ('billing_address_final', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('refunded', 'Refunded')], default='created', max_length=120)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=5.99, max_digits=100)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='addresses.address')),
                ('billing_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.billingprofile')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
                ('shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='addresses.address')),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
        ),
        migrations.CreateModel(
            name='InsuranceplanPurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=120)),
                ('refunded', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.billingprofile')),
                ('insuranceplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insuranceplans.insuranceplan')),
            ],
        ),
    ]
