# Generated by Django 4.1.6 on 2023-02-13 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_userapp_more_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformations',
            name='marital_state',
            field=models.CharField(choices=[('NDF', 'not define'), ('ML', 'male'), ('FML', 'female')], default='NDF', max_length=3, verbose_name='marital_state'),
        ),
    ]