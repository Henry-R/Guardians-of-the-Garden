# Generated by Django 5.0.2 on 2024-02-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sustainability', '0003_alter_plant_plant_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='plant_photo',
            field=models.ImageField(default='images/plant_default.jpg', upload_to='static/images'),
        ),
    ]
