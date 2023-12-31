# Generated by Django 4.1.7 on 2023-03-29 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FDApp', '0003_camera_gps_position_x_camera_gps_position_y'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='gps_position_x',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='camera',
            name='gps_position_y',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='platformuser',
            name='img',
            field=models.ImageField(blank=True, default='profile_pics/default.png', null=True, upload_to='profile_pics'),
        ),
    ]
