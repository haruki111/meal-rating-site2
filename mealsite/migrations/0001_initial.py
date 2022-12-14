# Generated by Django 3.2.15 on 2022-08-25 14:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('imageUrl', models.CharField(max_length=200)),
                ('countryOfOrigin', models.CharField(max_length=100)),
                ('typicalMealTime', models.IntegerField(choices=[(1, 'morning'), (2, 'afternoon'), (3, 'evening')])),
                ('dateAdded', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='MealRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('dateOfRating', models.DateTimeField(default=django.utils.timezone.now)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mealsite.meal')),
            ],
        ),
    ]
