# Generated by Django 3.2.7 on 2021-10-04 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash on Delivery', 'Cash on Delivery'), ('Khalti', 'Khalti')], default='Cash on Delivery', max_length=50),
        ),
    ]