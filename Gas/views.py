from django.shortcuts import render, redirect
from django.contrib import messages
from Gas.models import Gas
from .forms import GasForm

# Create your views here.


def gascrud(request):

    gasescrud = Gas.objects.all()

    return render(
        request,
        "Gas/gascrud.html",
        {"gasescrud": gasescrud},
    )


def creargas(request):
    if request.method == "POST":
        gas_form = GasForm(request.POST)
        if gas_form.is_valid():
            gas_form.save()
            return redirect("/Gas/Crud/CrearGas/")
        else:
            messages.error(request, "Error en el ingreso de datos")
            return redirect("/Gas/Crud/CrearGas/")
    else:
        gas_form = GasForm()

    return render(request, "Gas/creargas.html", {"form": gas_form})


def editargas(request, id):
    try:
        gas = Gas.objects.get(idcrianza=id)
    except Gas.DoesNotExist:
        messages.error(request, "No existe el Consumo de gas a editar")
        return redirect("/Gasas/Crud/EditarGas/")

    if request.method == "POST":
        gas_form = GasForm(request.POST, instance=gas)
        if gas_form.is_valid():
            gas_form.save()
            return redirect("/Gas/Crud/")
    else:
        gas_form = GasForm(instance=gas)

    return render(request, "Gas/editargas.html", {"form": gas_form})


def eliminargas(request, id):
    gas = Gas.objects.get(idcrianza=id)
    gas.delete()

    return redirect("/Gas/Crud")


def listargas(request):

    gases = Gas.objects.select_related("idcrianza")

    return render(request, "Gas/listagas.html", {"gases": gases})
