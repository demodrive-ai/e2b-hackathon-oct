# Generated by Django 5.1.1 on 2024-10-06 00:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogchecker", "0004_remove_e2brunoutput_blog_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="is_analyzed",
            field=models.BooleanField(default=False),
        ),
    ]
