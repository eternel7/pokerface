# Generated by Django 2.0.8 on 2019-01-26 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatrooms', '0004_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='answer_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_answer_by', to='chatrooms.Post'),
        ),
    ]
