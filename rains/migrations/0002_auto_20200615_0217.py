# Generated by Django 3.0.7 on 2020-06-15 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0002_auto_20200615_0217'),
        ('rains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rain',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rains', to='fields.Field'),
        ),
    ]