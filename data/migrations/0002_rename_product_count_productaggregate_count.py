# Generated by Django 3.2.7 on 2021-09-27 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productaggregate',
            old_name='product_count',
            new_name='count',
        ),
    ]
