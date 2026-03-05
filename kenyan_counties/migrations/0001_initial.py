from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="County",
            fields=[
                ("code", models.IntegerField(help_text="Unique county code (1-47)", primary_key=True, serialize=False, unique=True)),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "verbose_name_plural": "counties",
                "ordering": ["code"],
            },
        ),
        migrations.CreateModel(
            name="Constituency",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("county", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="constituencies", to="kenyan_counties.county")),
            ],
            options={
                "verbose_name_plural": "constituencies",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Ward",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("constituency", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="wards", to="kenyan_counties.constituency")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AlterUniqueTogether(
            name="constituency",
            unique_together={("county", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="ward",
            unique_together={("constituency", "name")},
        ),
    ]
