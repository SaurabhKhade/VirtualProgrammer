# Generated by Django 3.1.3 on 2020-11-13 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201112_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='comment',
            field=models.TextField(unique=True),
        ),
    ]