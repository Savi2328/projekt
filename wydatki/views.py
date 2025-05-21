from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Wydatek
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import WydatekForm
from django.views.generic import DetailView
from django.views.generic import TemplateView


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
    wydatki = Wydatek.objects.all().order_by('-wydatek_data')
    return render(
        request, 'wydatki/lista_wydatkow.html', {'wydatki':wydatki}
    )

def wydatek_szczegoly(request, pk):
    wydatek = get_object_or_404(Wydatek, pk=pk)
    return render(request, 'wydatki/wydatek_szczegoly.html', {'wydatek':wydatek})


def wydatek_nowy(request):
    if request.method == "POST":
        form = WydatekForm(request.POST, request.FILES)
        if form.is_valid():
            wydatek = form.save(commit=False)
            wydatek.author = request.user
            wydatek.wydatek_data = timezone.now()
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

# Create your views here.
