from .models import Bencina
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

def listado(request):
    bencinas = Bencina.objects.all().order_by('-fecha_creacion')

    return render(request, 'bencina_listado.html', {
        'bencinas': bencinas
    })



def eliminar_bencina(request, id):
    registro = get_object_or_404(Bencina, id=id)
    registro.delete()
    return redirect('bencina_listado')  # ajusta al nombre de tu vista listado