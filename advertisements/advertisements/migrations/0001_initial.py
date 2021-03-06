# Generated by Django 2.1.5 on 2019-01-28 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.PositiveIntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisements.Category')),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.Category'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisements.SubCategory'),
        ),
    ]
