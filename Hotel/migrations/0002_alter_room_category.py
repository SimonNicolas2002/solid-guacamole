# Generated by Django 5.0.4 on 2024-05-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='category',
            field=models.CharField(choices=[('Single', 'Standard Rooms'), ('Suite', 'Suites'), ('Double', 'Double Rooms')], max_length=50),
        ),
    ]