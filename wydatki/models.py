from django.db import models
from django.utils import timezone

class Wydatek(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    wydatek_nazwa = models.CharField(
        "Nazwa wydatku",
        max_length=200,
        default=''
    )
    wydatek_kwota = models.DecimalField(
        "Kwota wydatku",
        max_digits=8,
        decimal_places=2,
        default=0
    )
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

    #SK
    image = models.ImageField(null=True, blank=True, upload_to='images/')


    def __str__(self):
        return (
            f"{self.wydatek_nazwa}"
            f"({self.wydatek_rodzaj or 'brak'}) -"
            f"{self.wydatek_kwota} zł "
            f"({self.wydatek_data})"
        )


class Kategoria(models.Model):
    NAZWY_KATEGORIA= [
        ('oplaty_stale', 'Opłaty stałe'),
        ('jedzenie', 'Jedzenie'),
        ('przyjemnosci', 'Przyjemności'),
        ('rozwoj', 'Rozwój'),
        ('inwestycje', 'Inwestycje'),
        ('inne', 'Inne'),
    ]
    slug = models.CharField(max_length=30, choices=NAZWY_KATEGORIA, unique=True)
    nazwa = models.CharField(max_length=100)

    ICON_MAP = {
        'oplaty_stale: bi bi-cash-stack',
    }



# Create your models here.
