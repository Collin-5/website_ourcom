# Generated by Django 4.0.3 on 2022-03-07 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(help_text='can be empty', upload_to='uploads/', verbose_name='image'),
        ),
    ]