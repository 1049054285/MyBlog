# Generated by Django 2.0.3 on 2018-03-23 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180323_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='siteSubCategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.SiteSubCategory'),
        ),
    ]
