from django.db import models
from django.utils import timezone



class Kategoria(models.Model):
    ICON_MAP= [
        ('oplaty_stale', 'Opłaty stałe'),
        ('jedzenie', 'Jedzenie'),
        ('przyjemnosci', 'Przyjemności'),
        ('rozwoj', 'Rozwój'),
        ('inwestycje', 'Inwestycje'),
        ('inne', 'Inne'),
    ]
    slug = models.CharField(max_length=30, choices=ICON_MAP, unique=True)
    nazwa = models.CharField(max_length=100)

    ICON_MAP = {
        'oplaty_stale': 'bi bi-cash-stack',
        'jedzenie': 'egg-fill',
        'przyjemnosci': 'bi bi-heart-fill',
        'rozwoj': 'bi bi-lightbulb',
        'inwestycje': 'bi bi-graph-up-arrow',
        'inne': 'bi bi-question-circle'
    }
    @property
    def ikona(self):
        return self.ICON_MAP.get(self.slug, 'bi bi-question-circle')

    def __str__(self):
        return self.nazwa


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
    wydatek_rodzaj = models.ForeignKey(
        'Kategoria',
        verbose_name="Kategoria wydatku",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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
            f"({self.wydatek_rodzaj.nazwa if self.wydatek_rodzaj else 'brak'}) -"
            f"{self.wydatek_kwota} zł "
            f"({self.wydatek_data})"
        )

# Create your models here.
