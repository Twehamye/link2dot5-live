# Generated by Django 4.1.2 on 2023-08-17 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans_app', '0007_remove_loanapplication_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='Accepted'),
        ),
    ]
