# Generated by Django 4.1.3 on 2022-12-05 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_groupprofits_value_total_alter_groupprofits_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="groupprofits",
            name="value_total",
        ),
    ]
