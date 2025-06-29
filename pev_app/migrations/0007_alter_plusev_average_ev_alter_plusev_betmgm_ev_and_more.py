# Generated by Django 4.1 on 2024-04-15 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pev_app", "0006_plusev_betparx_ev"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plusev",
            name="average_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="betmgm_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="betmgm_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="betparx_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="betparx_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="betrivers_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="betrivers_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="bovada_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="bovada_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="draftkings_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="draftkings_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="espnbet_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="espnbet_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="fanduel_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="fanduel_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="hardrockbet_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="hardrockbet_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="pinnacle_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="pinnacle_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="superbook_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="superbook_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="tipico_us_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="tipico_us_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="williamhill_us_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="williamhill_us_odds",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="windcreek_ev",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="plusev",
            name="windcreek_odds",
            field=models.FloatField(null=True),
        ),
    ]
