# Generated by Django 3.2.16 on 2023-01-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20230102_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrator'), ('member', 'Member'), ('Supervisor', 'Supervisor'), ('Teamleader', 'Teamleader')], default='member', max_length=100),
        ),
        migrations.AlterField(
            model_name='membership',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrator'), ('member', 'Member'), ('Supervisor', 'Supervisor'), ('Teamleader', 'Teamleader')], max_length=100),
        ),
    ]
