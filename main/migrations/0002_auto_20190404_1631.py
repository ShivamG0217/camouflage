# Generated by Django 2.1.7 on 2019-04-04 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('key', models.TextField()),
                ('img', models.FileField(upload_to='hidemessage/')),
            ],
        ),
        migrations.DeleteModel(
            name='Tutorials',
        ),
    ]
