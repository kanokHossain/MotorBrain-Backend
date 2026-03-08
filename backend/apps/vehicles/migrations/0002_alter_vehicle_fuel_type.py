from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='fuel_type',
            field=models.CharField(
                choices=[
                    ('petrol', 'Petrol'),
                    ('diesel', 'Diesel'),
                    ('electric', 'Electric'),
                    ('hybrid', 'Hybrid'),
                    ('cng', 'CNG'),
                    ('lpg', 'LPG'),
                    ('octane', 'Octane'),
                ],
                default='petrol',
                max_length=20,
            ),
        ),
    ]
