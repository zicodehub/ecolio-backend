# Generated by Django 3.2.6 on 2021-08-16 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_clientdb_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdb',
            name='db_alias',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
