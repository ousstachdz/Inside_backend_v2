# Generated by Django 4.1.6 on 2023-02-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messanger', '0002_conversation_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
