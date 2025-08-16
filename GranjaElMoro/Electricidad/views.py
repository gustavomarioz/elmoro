from django.shortcuts import render, redirect
from django.contrib import messages
from Electricidad.models import Electricidad
from .forms import LuzForm

# Create your views here.


def luzcrud(request):

    lucescrud = Electricidad.objects.all()

    return render(
        request,
        "Electricidad/luzcrud.html",
        {"lucescrud": lucescrud},
    )


def crearluz(request):
    if request.method == "POST":
        luz_form = LuzForm(request.POST)
        if luz_form.is_valid():
            luz_form.save()
            return redirect("/Electricidad/Crud/CrearLuz/")
        else:
            messages.error(request, "Error en el ingreso de datos")
            return redirect("/Electricidad/Crud/CrearLuz/")
    else:
        luz_form = LuzForm()

    return render(request, "Electricidad/crearluz.html", {"form": luz_form})


def editarluz(request, id):
    try:
        luz = Electricidad.objects.get(idcrianza=id)
    except Electricidad.DoesNotExist:
        messages.error(request, "No existe el Consumo de electricidad a editar")
        return redirect("/Electricidad/Crud/EditarLuz/")

    if request.method == "POST":
        luz_form = LuzForm(request.POST, instance=luz)
        if luz_form.is_valid():
            luz_form.save()
            return redirect("/Electricidad/Crud/")
    else:
        luz_form = LuzForm(instance=luz)

    return render(request, "Electricidad/editarluz.html", {"form": luz_form})


def eliminarluz(request, id):
    luz = Electricidad.objects.get(idcrianza=id)
    luz.delete()

    return redirect("/Electricidad/Crud")


def listarluz(request):

    luces = Electricidad.objects.select_related("idcrianza")

    return render(request, "Electricidad/listaluz.html", {"luces": luces})
