# Generated by Django 5.0.4 on 2024-06-01 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0005_alter_room_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='num_beds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='num_toilets',
            field=models.IntegerField(default=0),
        ),
    ]
