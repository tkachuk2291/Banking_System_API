# Generated by Django 5.0.6 on 2024-06-08 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Deposit",
            fields=[
                (
                    "account_id",
                    models.AutoField(db_column="account_id", primary_key=True, serialize=False),
                ),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Withdrawal",
            fields=[
                (
                    "account_id",
                    models.AutoField(db_column="account_id", primary_key=True, serialize=False),
                ),
                ("amount", models.FloatField()),
            ],
        ),
    ]
