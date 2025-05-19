from django.db import models
from django.utils import timezone

class Wydatek(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    wydatek_nazwa = models.CharField(
        "Nazwa wydatku",
        max_length=200
    )
    wydatek_kwota = models.DecimalField(
        "Kwota",
        max_digits=8,
        decimal_places=2)
    wydatek_rodzaj = models.CharField(
        "Rodzaj wydatku",
        max_length=100,
        blank=True,
        default=""
    )
    wydatek_data = models.DateTimeField(
        "Data wydatku",
        default=timezone.now
    )


    def __str__(self):
        return (
            f"{self.wydatek_nazwa}"
            f"({self.wydatek_rodzaj or 'brak'}) -"
            f"{self.wydatek_kwota} zł "
            f"({self.wydatek_data}"
        )





# Create your models here.
