$(document).ready(() => {
  var ruta = window.location.pathname;
  if ((ruta.substring(0, ruta.lastIndexOf('/')) == "/Aportes/Crud/CrearAporte") ||
    (ruta.substring(0, ruta.lastIndexOf('/')) == "/Aportes/Crud/EditarAporte") ||
    (ruta.substring(0, ruta.lastIndexOf('/')) == "/Gas/Crud/CrearGas") ||
    (ruta.substring(0, ruta.lastIndexOf('/')) == "/Gas/Crud/EditarGas") ||
    (ruta.substring(0, ruta.lastIndexOf('/')) == "/Electricidad/Crud/CrearLuz") ||
    (ruta.substring(0, ruta.lastIndexOf('/')) == "/Electricidad/Crud/EditarLuz") ||
    (ruta.substring(0, ruta.lastIndexOf('/')) == "/Resultados/ResultadosXCrianza")) {
    return
  }

  $('th').each(function () {
    $(this).hover(function () {
      if (($(this).index() != 6 || ruta != "/Repartos/Crud/") &&
        ($(this).index() != 6 || ruta != "/Aportes/Crud/") &&
        ($(this).index() != 5 || ruta != "/Gas/Crud/") &&
        ($(this).index() != 6 || ruta != "/Electricidad/Crud/") &&
        ($(this).index() != 8 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos") &&
        ($(this).index() != 8 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Cobranzas") &&
        ($(this).index() != 10 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Resultados") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos/CostosXCrianza") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Cobranzas/CobrosXCrianza") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos/CostosXCrianza/CostosXCuenta")) {
        $(this).addClass('resaltar');
      }
    }, function () {
      if (($(this).index() != 6 || ruta != "/Repartos/Crud/") &&
        ($(this).index() != 6 || ruta != "/Aportes/Crud/") &&
        ($(this).index() != 5 || ruta != "/Gas/Crud/") &&
        ($(this).index() != 6 || ruta != "/Electricidad/Crud/") &&
        ($(this).index() != 8 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos") &&
        ($(this).index() != 8 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Cobranzas") &&
        ($(this).index() != 10 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Resultados") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos/CostosXCrianza") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Cobranzas/CobrosXCrianza") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos/CostosXCrianza/CostosXCuenta")) {
        $(this).removeClass('resaltar');
      }
    });

    $(this).click(function () {
      if (($(this).index() != 6 || ruta != "/Repartos/Crud/") &&
        ($(this).index() != 6 || ruta != "/Aportes/Crud/") &&
        ($(this).index() != 5 || ruta != "/Gas/Crud/") &&
        ($(this).index() != 6 || ruta != "/Electricidad/Crud/") &&
        ($(this).index() != 8 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos") &&
        ($(this).index() != 8 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Cobranzas") &&
        ($(this).index() != 10 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Resultados") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos/CostosXCrianza") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Cobranzas/CobrosXCrianza") &&
        ($(this).index() != 5 || ruta.substring(0, ruta.lastIndexOf('/')) != "/Costos/CostosXCrianza/CostosXCuenta")) {
        var table = $(this).parents('table').eq(0)
        var rows = table.find('tbody tr').toArray().sort(comparer($(this).index()))
        this.asc = !this.asc
        if (!this.asc) {
          rows = rows.reverse()
        }
        for (var i = 0; i < rows.length; i++) {
          table.append(rows[i])
        }
        setIcon($(this), this.asc);
      }
    });

    function comparer(index) {
      return function (a, b) {
        var valA = getCellValue(a, index);
        var valB = getCellValue(b, index);
        var valorA, valorB

        if (valA.includes("<a href=")) {
          valA = valA.substring(valA.indexOf(">") + 1, valA.lastIndexOf("<"))
        }
        if (valB.includes("<a href=")) {
          valB = valB.substring(valB.indexOf(">") + 1, valB.lastIndexOf("<"))
        }

        if (IsNum(valA.trim()) && IsNum(valB.trim())) {
          var cad1, cad2
          cad1 = valA.replaceAll(".", "");
          if (valA.indexOf(",") != -1) {
            cad2 = cad1.replaceAll(",", ".");
            valorA = parseFloat(cad2);
          }
          else {
            valorA = parseInt(cad1);
          }
          cad1 = valB.replaceAll(".", "");
          if (valB.indexOf(",") != -1) {
            cad2 = cad1.replaceAll(",", ".");
            valorB = parseFloat(cad2);
          }
          else {
            valorB = parseInt(cad1);
          }
          return valorA - valorB;
        }
        else if (IsDate(valA.trim()) && IsDate(valB.trim())) {
          valorA = ConvertDate(valA.trim())
          valorB = ConvertDate(valB.trim())
          return valorA - valorB;
        }
        else {
          return valA.localeCompare(valB);
        }
      }
    }

    function getCellValue(row, index) {
      return $(row).children('td').eq(index).html()
    }

    function IsNum(valor) {
      var caracteres = "0123456789.,";
      for (let i = 0; i < valor.length; i++) {
        if (caracteres.indexOf(valor.charAt(i), 0) == -1) {
          return false;
        }
      }
      return true;
    }

    function IsDate(valor) {
      if (valor.length != 10) {
        return false
      }

      var caracteres = "0123456789/";
      barras = 0;
      for (let i = 0; i < valor.length; i++) {
        if (caracteres.indexOf(valor.charAt(i), 0) == -1) {
          return false;
        }
        else if (valor.charAt(i) == "/") {
          barras++;
        }
      }

      if (barras != 2) {
        return false;
      }

      var primero = valor.indexOf('/');
      if (primero == 2) {
        var segundo = valor.indexOf('/', primero + 1);
        if (segundo == 5) {
          return true;
        }
        else {
          return false;
        }
      }
      else {
        return false;
      }
    }

    function ConvertDate(valor) {
      var primero = valor.indexOf('/');
      var inicio = primero + 1;
      var segundo = valor.indexOf('/', inicio);
      var fin = segundo + 1;

      dia = valor.substring(0, primero);
      mes = valor.substring(inicio, segundo);
      anio = valor.substring(fin);

      return parseInt(anio + mes + dia);
    }

    function setIcon(element, asc) {
      $("th").each(function (index) {
        $(this).removeClass("sorting");
        $(this).removeClass("asc");
        $(this).removeClass("desc");
      });
      element.addClass("sorting");
      if (asc) element.addClass("asc");
      else element.addClass("desc");
    }
  });
});
