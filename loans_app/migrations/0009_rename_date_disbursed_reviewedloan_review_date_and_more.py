# Generated by Django 4.1.2 on 2023-08-18 07:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans_app', '0008_loanapplication_accepted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewedloan',
            old_name='date_disbursed',
            new_name='review_date',
        ),
        migrations.RemoveField(
            model_name='reviewedloan',
            name='interest_rate',
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='Registered_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 8, 18, 7, 20, 37, 831637, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='collateral_name',
            field=models.CharField(default='cara', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='guarantor1_ID',
            field=models.CharField(default=2222, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='guarantor2_ID',
            field=models.CharField(default=2222, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='loan_period',
            field=models.PositiveIntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='loan_type',
            field=models.CharField(choices=[('Kagwirawo', 'Kagwirawo'), ('Longterm loan', 'Longterm loan')], default='kagwirawo', max_length=50),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disbursed_amount', models.PositiveIntegerField()),
                ('loan_period', models.PositiveIntegerField()),
                ('interest_rate', models.PositiveIntegerField()),
                ('disbursed_date', models.DateTimeField(auto_now_add=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans_app.reviewedloan')),
            ],
        ),
        migrations.AlterField(
            model_name='loanpayment',
            name='loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans_app.loan'),
        ),
    ]
