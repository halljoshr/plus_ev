import uuid

from django.db import models


# Create your models here.
class PlusEV(models.Model):
    pair_id = models.UUIDField(default=uuid.uuid4, editable=False)
    sport = models.CharField(max_length=20)
    market = models.CharField(max_length=40)
    date = models.DateTimeField()
    event = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    outcome = models.CharField(max_length=100)
    point = models.FloatField()
    betmgm_ev = models.FloatField(null=True)
    draftkings_ev = models.FloatField(null=True)
    fanduel_ev = models.FloatField(null=True)
    betrivers_ev = models.FloatField(null=True)
    bovada_ev = models.FloatField(null=True)
    pinnacle_ev = models.FloatField(null=True)
    williamhill_us_ev = models.FloatField(null=True)
    windcreek_ev = models.FloatField(null=True)
    superbook_ev = models.FloatField(null=True)
    hardrockbet_ev = models.FloatField(null=True)
    betparx_ev = models.FloatField(null=True)
    tipico_us_ev = models.FloatField(null=True)
    espnbet_ev = models.FloatField(null=True)
    average_ev = models.FloatField(null=True)
    betmgm_odds = models.FloatField(null=True)
    draftkings_odds = models.FloatField(null=True)
    fanduel_odds = models.FloatField(null=True)
    betrivers_odds = models.FloatField(null=True)
    bovada_odds = models.FloatField(null=True)
    pinnacle_odds = models.FloatField(null=True)
    williamhill_us_odds = models.FloatField(null=True)
    windcreek_odds = models.FloatField(null=True)
    superbook_odds = models.FloatField(null=True)
    hardrockbet_odds = models.FloatField(null=True)
    betparx_odds = models.FloatField(null=True)
    tipico_us_odds = models.FloatField(null=True)
    espnbet_odds = models.FloatField(null=True)
    average_odds = models.FloatField()
    win_prob = models.FloatField()

    def __str__(self):
        return (
            self.description
            + " "
            + self.outcome
            + " "
            + str(self.point)
            + " "
            + str(self.date)
        )


class PlacedBet(models.Model):
    plus_ev = models.ForeignKey(PlusEV, on_delete=models.CASCADE)
    bet_amount = models.FloatField()
    placed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plus_ev.description} bet on {self.placed_date}"
