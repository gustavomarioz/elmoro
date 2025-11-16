from datetime import datetime


def crianzavalida(c):
    if c.isdigit():
        if int(c) >= 17 and int(c) < 1000:
            return True
        else:
            return False
    else:
        return False


def fechavalida(f):
    if len(f) < 6 or len(f) > 10:
        return False

    caracteres = "0123456789/"
    barras = 0
    for i in range(0, len(f)):
        if caracteres.find(f[i], 0) == -1:
            return False
        elif f[i] == "/":
            barras += 1

    if barras != 2:
        return False

    primero = f.find("/")
    if primero > 0 and primero < 3:
        inicio = primero + 1
        segundo = f.find("/", inicio)
        if segundo > 2 and segundo < 6:
            fin = segundo + 1
            ldia = len(f[0:primero])
            lmes = len(f[inicio:segundo])
            lanio = len(f[fin:])
            if ldia >= 1 and ldia <= 2:
                if lmes >= 1 and lmes <= 2:
                    if lanio == 2 or lanio == 4:
                        dia = f[0:primero]
                        mes = f[inicio:segundo]
                        anio = f[fin:]
                        if fechacorrecta(dia, mes, anio):
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def fechacorrecta(di, me, an):
    d = int(di)
    m = int(me)
    a = int(prepararanio(an)) if len(an) == 2 else int(an)

    if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
        if d >= 1 and d <= 31:
            return True
        else:
            return False
    elif m == 4 or m == 6 or m == 9 or m == 11:
        if d >= 1 and d <= 30:
            return True
        else:
            return False
    elif m == 2:
        if d >= 1 and d <= 28:
            return True
        elif d == 29:
            if a % 4 == 0 and (a % 100 != 0 or a % 400 == 0):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def prepararfecha(f):
    primero = f.find("/")
    inicio = primero + 1
    segundo = f.find("/", inicio)
    fin = segundo + 1

    dia = f[0:primero]
    if len(dia) < 2:
        dia = "0" + dia

    mes = f[inicio:segundo]
    if len(mes) < 2:
        mes = "0" + mes

    anio = f[fin:]
    if len(anio) == 2:
        año = prepararanio(anio)
    else:
        año = anio

    return dia + "/" + mes + "/" + año


def prepararanio(a):
    ahora = datetime.now()
    hoy = ahora.strftime("%d/%m/%Y")
    siglo = hoy[6:8]
    decada = hoy[8:]
    if int(a) <= int(decada) or a[0:1] == decada[0:1]:
        anio = siglo + a
    else:
        anio = str(int(siglo) - 1) + a

    return anio


def importevalido(imp):
    coma = imp.find(",", 0)
    inicio = coma + 1
    if coma != -1:
        dec = imp[inicio:]
        if not dec.isdigit():
            return False
        entera = imp[0:coma]
        if len(entera) == 0:
            return False
    else:
        entera = imp

    if len(entera) == 1 and entera == "0" and int(dec) == 0:
        return False

    caracteres = "0123456789."
    digitos = 0
    puntos = 0
    for i in range(len(entera) - 1, -1, -1):
        if caracteres.find(entera[i], 0) == -1:
            return False
        elif entera[i] == ".":
            if digitos == 3:
                puntos += 1
                digitos = 0
            else:
                return False
        else:
            digitos += 1

    if puntos == 0:
        if digitos == 0:
            return False
        else:
            return True
    elif puntos > 0:
        if digitos == 0:
            return False
        elif digitos > 3:
            return False
        else:
            return True
    else:
        return False


def stringadouble(i):
    return format(i).replace(".", "").replace(",", ".")
