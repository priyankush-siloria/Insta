# Generated by Django 2.2.3 on 2019-07-27 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instaapp', '0002_userpackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.IntegerField(blank=True, null=True, verbose_name='user_account')),
                ('account_password', models.CharField(blank=True, max_length=100, null=True, verbose_name='user_package')),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
