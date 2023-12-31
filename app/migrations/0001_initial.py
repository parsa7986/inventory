# Generated by Django 4.2.2 on 2023-06-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('description', models.TextField()),
                ('prodapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('PS', 'Pistachio'), ('AL', 'Almond'), ('WL', 'Walnut'), ('HZ', 'Hazelnut'), ('DA', 'Dates')], max_length=2)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
    ]
