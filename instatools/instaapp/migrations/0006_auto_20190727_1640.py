# Generated by Django 2.2.3 on 2019-07-27 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instaapp', '0005_userinstadetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinstadetail',
            name='user',
        ),
        migrations.AddField(
            model_name='userinstadetail',
            name='insta_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instaapp.UserAccounts', verbose_name='Insta User'),
        ),
    ]