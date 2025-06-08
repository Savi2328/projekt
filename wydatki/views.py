from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Wydatek, Kategoria
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import WydatekForm
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import datetime
import json

class Image(TemplateView):
    form_class = WydatekForm
    template_name = 'wydatki/image.html'
    succes_url = reverse_lazy('lista_wydatkow')

    def post(self,request,*args,**kwargs):
        form = WydatekForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('image_display',kwargs={'pk':obj.id}))

        context = self.get_contaxt_data(form=form)
        return self.render_to_response(context)

    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)

class ImageDisplay(DetailView):
    model = Wydatek
    template_name = 'wydatki/image_display.html'
    context_object_name = 'wydatek'

def lista_wydatkow(request):

    wszystkie_kategorie = Kategoria.objects.all().order_by('nazwa')

    wybrane_slugi = request.GET.getlist('kategorie')

    qs = Wydatek.objects.all().order_by('-wydatek_data')

    if wybrane_slugi:
        qs = qs.filter(wydatek_rodzaj__slug__in=wybrane_slugi)

    ostatnie = qs[:5]

    podsumowania = (
        Wydatek.objects
             .annotate(miesiac=TruncMonth('wydatek_data'))
             .values('miesiac')
             .annotate(suma=Sum('wydatek_kwota'))
             .order_by('-miesiac')
    )

    labels = [p['miesiac'].strftime('%B %Y') for p in podsumowania]
    data   = [float(p['suma']) for p in podsumowania]

    context = {
        'wszystkie_kategorie': wszystkie_kategorie,
        'wybrane_slugi': wybrane_slugi,
        'wydatki': ostatnie,
        'podsumowania': podsumowania,
        'chart_labels': json.dumps(labels),
        'chart_data':   json.dumps(data),
    }
    return render(request, 'wydatki/lista_wydatkow.html', context)

def wydatek_szczegoly(request, pk):
    wydatek = get_object_or_404(Wydatek, pk=pk)
    return render(request, 'wydatki/wydatek_szczegoly.html', {'wydatek':wydatek})


def wydatek_nowy(request):
    if request.method == "POST":
        form = WydatekForm(request.POST, request.FILES)
        if form.is_valid():
            wydatek = form.save(commit=False)
            wydatek.author = request.user
            #wydatek.wydatek_data = timezone.now()
            wydatek.save()
            return redirect('wydatek_szczegoly', pk=wydatek.pk)
    else:
        form=WydatekForm()
    return render(request, 'wydatki/wydatek_edycja.html', {'form':form})


def wydatek_edycja(request, pk):
    wydatek = get_object_or_404(Wydatek, pk=pk)
    if request.method == "POST":
        form = WydatekForm(request.POST, request.FILES, instance=wydatek)
        if form.is_valid():
            wydatek = form.save(commit=False)
            wydatek.author = request.user
            wydatek.wydatek_data = timezone.now()
            wydatek.save()
            return redirect('wydatek_szczegoly', pk=wydatek.pk)
    else:
        form=WydatekForm(instance=wydatek)
    return render(request, 'wydatki/wydatek_edycja.html', {'form':form})


def podsumowanie_miesiaca(request, rok, miesiac):


    wszystkie_kategorie = Kategoria.objects.all().order_by('nazwa')

    wybrane_slugi = request.GET.getlist('kategorie')

    start = datetime.date(rok, miesiac, 1)
    if miesiac == 12:
        koniec = datetime.date(rok + 1, 1, 1)
    else:
        koniec = datetime.date(rok, miesiac + 1, 1)

    qs = Wydatek.objects.filter(
        wydatek_data__gte=start,
        wydatek_data__lt=koniec
    ).order_by('-wydatek_data')

    if wybrane_slugi:
        qs = qs.filter(wydatek_rodzaj__slug__in=wybrane_slugi)

    suma = qs.aggregate(total=Sum('wydatek_kwota'))['total'] or 0

    category_summary = (
        qs
        .values('wydatek_rodzaj__nazwa')
        .annotate(suma_kategorii=Sum('wydatek_kwota'))
    )

    labels = []
    data   = []
    for item in category_summary:
        nazwak = item['wydatek_rodzaj__nazwa'] or 'Brak kategorii'
        labels.append(nazwak)
        data.append(float(item['suma_kategorii'] or 0))

    labels_json = json.dumps(labels)
    data_json   = json.dumps(data)

    context = {
        'rok': rok,
        'miesiac': start,
        'wszystkie_kategorie': wszystkie_kategorie,
        'wybrane_slugi': wybrane_slugi,
        'wydatki': qs,
        'suma': suma,
        'chart_labels_pie': labels_json,
        'chart_data_pie': data_json,
    }
    return render(request, 'wydatki/podsumowanie_miesiaca.html', context)

# Create your views here.
