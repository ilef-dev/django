# Generated by Django 5.1.4 on 2024-12-14 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app8', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='user_solution',
            field=models.CharField(default='Нет ответа', max_length=255),
        ),
    ]