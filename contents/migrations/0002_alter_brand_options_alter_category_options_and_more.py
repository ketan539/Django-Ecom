# Generated by Django 4.1.7 on 2023-03-29 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'verbose_name_plural': '3) Brands'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '2) Categories'},
        ),
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name_plural': '4) Colors'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': '1) Products'},
        ),
        migrations.AlterModelOptions(
            name='smartphone',
            options={'verbose_name_plural': '5) Smartphones'},
        ),
        migrations.AlterModelOptions(
            name='smartphone_ram',
            options={'verbose_name_plural': '6) Smartphone RAM'},
        ),
        migrations.AlterModelOptions(
            name='smartphone_storage',
            options={'verbose_name_plural': '7) Smartphone Storage'},
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.product')),
                ('smartphone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.smartphone')),
                ('smartphone_ram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.smartphone_ram')),
                ('smartphone_storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.smartphone_storage')),
            ],
            options={
                'verbose_name_plural': '8) Products Attribute',
            },
        ),
    ]
