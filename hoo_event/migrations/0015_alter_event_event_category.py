# Generated by Django 4.2.6 on 2023-12-01 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hoo_event", "0014_alter_event_event_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_category",
            field=models.CharField(
                choices=[("1", "💡"), ("2", "🍔"), ("3", "🎉"), ("4", "🏟️")], max_length=2
            ),
        ),
    ]
