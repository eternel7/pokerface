# Generated by Django 2.0.8 on 2019-01-08 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatrooms', '0002_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='pdf_text',
            field=models.TextField(default=''),
        ),
    ]