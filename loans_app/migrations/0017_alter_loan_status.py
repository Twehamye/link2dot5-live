# Generated by Django 4.1.2 on 2023-09-05 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans_app', '0016_remove_loan_is_approved_alter_loan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('under_review', 'under_review'), ('approved', 'approved'), ('rejected', 'rejected')], default='under_review', max_length=20),
        ),
    ]
