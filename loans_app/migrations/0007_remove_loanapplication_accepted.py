# Generated by Django 4.1.2 on 2023-08-17 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans_app', '0006_remove_loanapplication_approved_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanapplication',
            name='accepted',
        ),
    ]