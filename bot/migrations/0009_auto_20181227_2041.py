# Generated by Django 2.1.4 on 2018-12-27 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_remove_user_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]