from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
#from clientes.models import Cliente
#from servicio_contable.models import ServicioContable   # ajusta si tu app se llama distinto
#from impuestos.models import Impuestos



def dashboard(request):
  #  total_clientes = Cliente.objects.count()

   # clientes_con_prevision = ServicioContable.objects.values('cliente').distinct().count()
   # clientes_con_impuestos = Impuestos.objects.values('cliente').distinct().count()

    # Si tienes un campo de deuda (ej: monto o deuda)
   # total_deuda = ServicioContable.objects.aggregate(total=Sum('deuda'))['total'] or 0

    return render(request, 'dashboard.html', {
      #  'total_clientes': total_clientes,
      #  'clientes_con_prevision': clientes_con_prevision,
      #  'clientes_con_impuestos': clientes_con_impuestos,
        #'total_deuda': total_deuda,
    })