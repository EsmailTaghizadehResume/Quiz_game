# Generated by Django 4.2.16 on 2024-11-07 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPasswords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
