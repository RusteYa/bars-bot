# Generated by Django 2.1.4 on 2018-12-27 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_auto_20181227_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.Question'),
        ),
    ]