(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    var ruta = window.location.pathname;
    var mensaje;
    if (ruta == "/Repartos/Crud/") {
        mensaje = "Reparto"
    }
    else if (ruta == "/Cobranzas/Crud/") {
        mensaje = "Cobranza"
    }
    else if (ruta == "/Aportes/Crud/") {
        mensaje = "Aporte"
    }
    else if (ruta == "/Gas/Crud/") {
        mensaje = "Consumo de Gas"
    }
    else if (ruta == "/Electricidad/Crud/") {
        mensaje = "Consumo de Electricidad"
    }

    btnEliminacion.forEach(btn => {
        btn.addEventListener("click", (e) => {
            const confirmacion = confirm("¿Realmente desea eliminar el " + mensaje + " ?");
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

})();
