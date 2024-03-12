# Generated by Django 4.2.10 on 2024-03-04 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_category_is_sub_category_sub_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='category',
            name='sub_category',
            field=models.ManyToManyField(blank=True, null=True, related_name='scategory', to='home.category'),
        ),
    ]
